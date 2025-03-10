"""
Utilities for creating bokeh Server instances.
"""
from __future__ import annotations

import asyncio
import datetime as dt
import gc
import html
import importlib
import logging
import os
import pathlib
import signal
import sys
import threading
import traceback
import uuid
import warnings
import weakref

from collections import OrderedDict
from contextlib import contextmanager
from functools import partial, wraps
from types import FunctionType, MethodType
from typing import (
    TYPE_CHECKING, Any, Callable, Dict, Mapping, Optional, Union,
)
from urllib.parse import urljoin, urlparse

import bokeh
import bokeh.command.util
import param
import tornado

# Bokeh imports
from bokeh.application import Application as BkApplication
from bokeh.application.handlers.code import (
    CodeHandler, _monkeypatch_io, patch_curdoc,
)
from bokeh.application.handlers.function import FunctionHandler
from bokeh.command.util import build_single_handler_application
from bokeh.core.templates import AUTOLOAD_JS
from bokeh.embed.bundle import Script
from bokeh.embed.elements import (
    html_page_for_render_items, script_for_render_items,
)
from bokeh.embed.util import RenderItem
from bokeh.io import curdoc
from bokeh.server.server import Server as BokehServer
from bokeh.server.urls import per_app_patterns
from bokeh.server.views.autoload_js_handler import (
    AutoloadJsHandler as BkAutoloadJsHandler,
)
from bokeh.server.views.doc_handler import DocHandler as BkDocHandler
from bokeh.server.views.static_handler import StaticHandler
# Tornado imports
from tornado.ioloop import IOLoop
from tornado.web import (
    HTTPError, RequestHandler, StaticFileHandler, authenticated,
)
from tornado.wsgi import WSGIContainer

# Internal imports
from ..config import config
from ..util import edit_readonly, fullpath
from .document import init_doc, unlocked, with_lock  # noqa
from .logging import (
    LOG_SESSION_CREATED, LOG_SESSION_DESTROYED, LOG_SESSION_LAUNCHING,
)
from .profile import profile_ctx
from .reload import autoreload_watcher
from .resources import (
    BASE_TEMPLATE, COMPONENT_PATH, ERROR_TEMPLATE, Resources, _env,
    bundle_resources, component_rel_path,
)
from .state import set_curdoc, state

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from bokeh.document import Document
    from bokeh.server.contexts import BokehSessionContext
    from bokeh.server.session import ServerSession
    from jinja2 import Template

    from ..template.base import BaseTemplate
    from ..viewable import Viewable, Viewer
    from .location import Location

    TViewable = Union[Viewable, Viewer, BaseTemplate]
    TViewableOrFunc = Union[TViewable, Callable[[], TViewable]]

#---------------------------------------------------------------------
# Private API
#---------------------------------------------------------------------

INDEX_HTML = os.path.join(os.path.dirname(__file__), '..', '_templates', "index.html")

def _origin_url(url: str) -> str:
    if url.startswith("http"):
        url = url.split("//")[1]
    return url

def _server_url(url: str, port: int) -> str:
    if url.startswith("http"):
        return '%s:%d%s' % (url.rsplit(':', 1)[0], port, "/")
    else:
        return 'http://%s:%d%s' % (url.split(':')[0], port, "/")

def _eval_panel(panel: 'TViewableOrFunc', server_id: str, title: str, location, doc: 'Document'):
    from ..pane import panel as as_panel
    from ..template import BaseTemplate

    with set_curdoc(doc):
        if isinstance(panel, (FunctionType, MethodType)):
            panel = panel()
        if isinstance(panel, BaseTemplate):
            doc = panel._modify_doc(server_id, title, doc, location)
        else:
            doc = as_panel(panel)._modify_doc(server_id, title, doc, location)
        return doc

def async_execute(func: Callable[..., None]) -> None:
    """
    Wrap async event loop scheduling to ensure that with_lock flag
    is propagated from function to partial wrapping it.
    """
    if not state.curdoc or not state.curdoc.session_context:
        ioloop = IOLoop.current()
        event_loop = ioloop.asyncio_loop # type: ignore
        if event_loop.is_running():
            ioloop.add_callback(func)
        else:
            event_loop.run_until_complete(func())
        return

    if isinstance(func, partial) and hasattr(func.func, 'lock'):
        unlock = not func.func.lock # type: ignore
    else:
        unlock = not getattr(func, 'lock', False)
    curdoc = state.curdoc
    @wraps(func)
    async def wrapper(*args, **kw):
        with set_curdoc(curdoc):
            return await func(*args, **kw)
    if unlock:
        wrapper.nolock = True # type: ignore
    state.curdoc.add_next_tick_callback(wrapper)

param.parameterized.async_executor = async_execute

def _initialize_session_info(session_context: 'BokehSessionContext'):
    from ..config import config
    session_id = session_context.id
    sessions = state.session_info['sessions']
    history = -1 if config._admin else config.session_history
    if not config._admin and (history == 0 or session_id in sessions):
        return

    state.session_info['total'] += 1
    if history > 0 and len(sessions) >= history:
        old_history = list(sessions.items())
        sessions = OrderedDict(old_history[-(history-1):])
        state.session_info['sessions'] = sessions
    sessions[session_id] = {
        'launched': dt.datetime.now().timestamp(),
        'started': None,
        'rendered': None,
        'ended': None,
        'user_agent': session_context.request.headers.get('User-Agent')
    }
    state.param.trigger('session_info')

state.on_session_created(_initialize_session_info)

#---------------------------------------------------------------------
# Bokeh patches
#---------------------------------------------------------------------

def server_html_page_for_session(
    session: 'ServerSession', resources: 'Resources', title: str,
    template: str | Template = BASE_TEMPLATE,
    template_variables: Optional[Dict[str, Any]] = None
) -> str:
    render_item = RenderItem(
        token = session.token,
        roots = session.document.roots,
        use_for_title = False,
    )

    if template_variables is None:
        template_variables = {}

    bundle = bundle_resources(session.document.roots, resources)
    return html_page_for_render_items(bundle, {}, [render_item], title,
        template=template, template_variables=template_variables)

def autoload_js_script(doc, resources, token, element_id, app_path, absolute_url):
    resources = Resources.from_bokeh(resources)
    bundle = bundle_resources(doc.roots, resources)

    render_items = [RenderItem(token=token, elementid=element_id, use_for_title=False)]
    bundle.add(Script(script_for_render_items({}, render_items, app_path=app_path, absolute_url=absolute_url)))

    return AUTOLOAD_JS.render(bundle=bundle, elementid=element_id)

def destroy_document(self, session):
    """
    Override for Document.destroy() without calling gc.collect directly.
    The gc.collect() call is scheduled as a task, ensuring that when
    multiple documents are destroyed in quick succession we do not
    schedule excessive garbage collection.
    """
    self.remove_on_change(session)
    del self._roots
    del self._theme
    del self._template
    self._session_context = None

    self.callbacks.destroy()
    self.models.destroy()
    self.modules.destroy()

    # Clear periodic callbacks
    for cb in state._periodic.get(self, []):
        cb.stop()

    # Clean up pn.state to avoid tasks getting executed on dead session
    for attr in dir(state):
        if not attr.startswith('_'):
            continue
        state_obj = getattr(state, attr)
        if isinstance(state_obj, weakref.WeakKeyDictionary) and self in state_obj:
            del state_obj[self]

    # Schedule GC
    at = dt.datetime.now() + dt.timedelta(seconds=5)
    state.schedule_task('gc.collect', gc.collect, at=at)


# Patch Srrver to attach task factory to asyncio loop
class Server(BokehServer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            _add_task_factory(self.io_loop.asyncio_loop) # type: ignore
        except Exception:
            pass

bokeh.server.server.Server = Server

# Patch Application to handle session callbacks
class Application(BkApplication):

    async def on_session_created(self, session_context):
        for cb in state._on_session_created:
            cb(session_context)
        await super().on_session_created(session_context)

    def initialize_document(self, doc):
        super().initialize_document(doc)
        if doc in state._templates:
            template = state._templates[doc]
            template.server_doc(title=template.title, location=True, doc=doc)

bokeh.command.util.Application = Application # type: ignore


class SessionPrefixHandler:

    @contextmanager
    def _session_prefix(self):
        prefix = self.request.uri.replace(self.application_context._url, '')
        if not prefix.endswith('/'):
            prefix += '/'
        base_url = urljoin('/', prefix)
        rel_path = '/'.join(['..'] * self.application_context._url.strip('/').count('/'))
        old_url, old_rel = state.base_url, state.rel_path

        # Handle autoload.js absolute paths
        abs_url = self.get_argument('bokeh-absolute-url', default=None)
        if abs_url is not None:
            app_path = self.get_argument('bokeh-app-path', default='')
            rel_path = abs_url.replace(app_path, '')

        with edit_readonly(state):
            state.base_url = base_url
            state.rel_path = rel_path
        try:
            yield
        finally:
            with edit_readonly(state):
                state.base_url = old_url
                state.rel_path = old_rel

# Patch Bokeh DocHandler URL
class DocHandler(BkDocHandler, SessionPrefixHandler):

    @authenticated
    async def get(self, *args, **kwargs):
        with self._session_prefix():
            session = await self.get_session()
            logger.info(LOG_SESSION_CREATED, id(session.document))
            with set_curdoc(session.document):
                if config.authorize_callback and not config.authorize_callback(state.user_info):
                    if config.auth_template:
                        with open(config.auth_template) as f:
                            template = _env.from_string(f.read())
                    else:
                        template = ERROR_TEMPLATE
                    page = template.render(
                        title='Panel: Authorization Error',
                        error_type='Authorization Error',
                        error='User is not authorized.',
                        error_msg=f'{state.user} is not authorized to access this application.'
                    )
                else:
                    resources = Resources.from_bokeh(self.application.resources())
                    page = server_html_page_for_session(
                        session, resources=resources, title=session.document.title,
                        template=session.document.template,
                        template_variables=session.document.template_variables
                    )
        self.set_header("Content-Type", 'text/html')
        self.write(page)

per_app_patterns[0] = (r'/?', DocHandler)

# Patch Bokeh Autoload handler
class AutoloadJsHandler(BkAutoloadJsHandler, SessionPrefixHandler):
    ''' Implements a custom Tornado handler for the autoload JS chunk

    '''

    async def get(self, *args, **kwargs) -> None:
        element_id = self.get_argument("bokeh-autoload-element", default=None)
        if not element_id:
            self.send_error(status_code=400, reason='No bokeh-autoload-element query parameter')
            return

        app_path = self.get_argument("bokeh-app-path", default="/")
        absolute_url = self.get_argument("bokeh-absolute-url", default=None)

        if absolute_url:
            server_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(absolute_url))
        else:
            server_url = None

        with self._session_prefix():
            session = await self.get_session()
            with set_curdoc(session.document):
                resources = Resources.from_bokeh(self.application.resources(server_url))
                js = autoload_js_script(
                    session.document, resources, session.token, element_id,
                    app_path, absolute_url
                )

        self.set_header("Content-Type", 'application/javascript')
        self.write(js)

per_app_patterns[3] = (r'/autoload.js', AutoloadJsHandler)


class ComponentResourceHandler(StaticFileHandler):
    """
    A handler that serves local resources relative to a Python module.
    The handler resolves a specific Panel component by module reference
    and name, then resolves an attribute on that component to check
    if it contains the requested resource path.

    /<endpoint>/<module>/<class>/<attribute>/<path>
    """

    _resource_attrs = [
        '__css__', '__javascript__', '__js_module__',  '_resources',
        '_css', '_js', 'base_css', 'css'
    ]

    def initialize(self, path: Optional[str] = None, default_filename: Optional[str] = None):
        self.root = path
        self.default_filename = default_filename

    def parse_url_path(self, path: str) -> str:
        """
        Resolves the resource the URL pattern refers to.
        """
        parts = path.split('/')
        if len(parts) < 4:
            raise HTTPError(400, 'Malformed URL')
        mod, cls, rtype, *subpath = parts
        try:
            module = importlib.import_module(mod)
        except ModuleNotFoundError:
            raise HTTPError(404, 'Module not found')
        try:
            component = getattr(module, cls)
        except AttributeError:
            raise HTTPError(404, 'Component not found')

        # May only access resources listed in specific attributes
        if rtype not in self._resource_attrs:
            raise HTTPError(403, 'Requested resource type not valid.')

        try:
            resources = getattr(component, rtype)
        except AttributeError:
            raise HTTPError(404, 'Resource type not found')

        # Handle template resources
        if rtype == '_resources':
            rtype = subpath[0]
            subpath = subpath[1:]
            if rtype not in resources:
                raise HTTPError(404, 'Resource type not found')
            resources = resources[rtype]
            rtype = f'_resources/{rtype}'

        if isinstance(resources, dict):
            resources = list(resources.values())
        elif isinstance(resources, (str, pathlib.PurePath)):
            resources = [resources]
        resources = [
            component_rel_path(component, resource).replace(os.path.sep, '/')
            for resource in resources
        ]

        rel_path = '/'.join(subpath)

        # Important: May only access resources explicitly listed on the component
        # Otherwise this potentially exposes all files to the web
        if rel_path not in resources:
            raise HTTPError(403, 'Requested resource was not listed.')

        if not module.__file__:
            raise HTTPError(404, 'Requested module does not reference a file.')

        return str(pathlib.Path(module.__file__).parent / rel_path)

    @classmethod
    def get_absolute_path(cls, root: str, path: str) -> str:
        return path

    def validate_absolute_path(self, root: str, absolute_path: str) -> str:
        if not os.path.exists(absolute_path):
            raise HTTPError(404)
        if not os.path.isfile(absolute_path):
            raise HTTPError(403, "%s is not a file", self.path)
        return absolute_path


def modify_document(self, doc: 'Document'):
    from bokeh.io.doc import set_curdoc as bk_set_curdoc

    from ..config import config

    logger.info(LOG_SESSION_LAUNCHING, id(doc))

    if config.autoreload:
        path = self._runner.path
        argv = self._runner._argv
        handler = type(self)(filename=path, argv=argv)
        self._runner = handler._runner

    module = self._runner.new_module()

    # If no module was returned it means the code runner has some permanent
    # unfixable problem, e.g. the configured source code has a syntax error
    if module is None:
        return

    # One reason modules are stored is to prevent the module
    # from being gc'd before the document is. A symptom of a
    # gc'd module is that its globals become None. Additionally
    # stored modules are used to provide correct paths to
    # custom models resolver.
    sys.modules[module.__name__] = module
    doc.modules._modules.append(module)

    try:
        old_doc = curdoc()
    except RuntimeError:
        old_doc = None
    bk_set_curdoc(doc)

    if config.autoreload:
        set_curdoc(doc)
        state.onload(autoreload_watcher)

    sessions = []

    try:
        def post_check():
            newdoc = curdoc()
            # Do not let curdoc track modules when autoreload is enabled
            # otherwise it will erroneously complain that there is
            # a memory leak
            if config.autoreload:
                newdoc.modules._modules = []

            # script is supposed to edit the doc not replace it
            if newdoc is not doc:
                raise RuntimeError("%s at '%s' replaced the output document" % (self._origin, self._runner.path))

        def handle_exception(handler, e):
            from bokeh.application.handlers.handler import handle_exception

            from ..pane import HTML

            # Clean up
            del sys.modules[module.__name__]

            if hasattr(doc, 'modules'):
                doc.modules._modules.remove(module)
            else:
                doc._modules.remove(module)
            bokeh.application.handlers.code_runner.handle_exception = handle_exception
            tb = html.escape(traceback.format_exc())

            # Serve error
            HTML(
                f'<b>{type(e).__name__}</b>: {e}</br><pre style="overflow-y: scroll">{tb}</pre>',
                css_classes=['alert', 'alert-danger'], sizing_mode='stretch_width'
            ).servable()

        if config.autoreload:
            bokeh.application.handlers.code_runner.handle_exception = handle_exception

        state._launching.append(doc)
        with _monkeypatch_io(self._loggers):
            with patch_curdoc(doc):
                with profile_ctx(config.profiler) as sessions:
                    self._runner.run(module, post_check)

        def _log_session_destroyed(session_context):
            logger.info(LOG_SESSION_DESTROYED, id(doc))

        doc.on_session_destroyed(_log_session_destroyed)
        doc.destroy = partial(destroy_document, doc) # type: ignore
    finally:
        state._launching.remove(doc)
        if config.profiler:
            try:
                path = doc.session_context.request.path
                state._profiles[(path, config.profiler)] += sessions
                state.param.trigger('_profiles')
            except Exception:
                pass
        if old_doc is not None:
            bk_set_curdoc(old_doc)

CodeHandler.modify_document = modify_document # type: ignore

# Copied from bokeh 2.4.0, to fix directly in bokeh at some point.
def create_static_handler(prefix, key, app):
    # patch
    key = '/__patchedroot' if key == '/' else key

    route = prefix
    route += "/static/(.*)" if key == "/" else key + "/static/(.*)"
    if app.static_path is not None:
        return (route, StaticFileHandler, {"path" : app.static_path})
    return (route, StaticHandler, {})

bokeh.server.tornado.create_static_handler = create_static_handler

#---------------------------------------------------------------------
# Async patches
#---------------------------------------------------------------------

# Bokeh 2.4.x patches the asyncio event loop policy but Tornado 6.1
# support the WindowsProactorEventLoopPolicy so we restore it,
# unless we detect we are running on jupyter_server.
if (
    sys.platform == 'win32' and
    sys.version_info[:3] >= (3, 8, 0) and
    tornado.version_info >= (6, 1) and
    type(asyncio.get_event_loop_policy()) is asyncio.WindowsSelectorEventLoopPolicy and
    (('jupyter_server' not in sys.modules and
      'jupyter_client' not in sys.modules) or
     'pytest' in sys.modules)
):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

def _add_task_factory(loop):
    """
    Adds a Task factory to the asyncio IOLoop that ensures child tasks
    have access to their parent.
    """
    if getattr(loop, '_has_panel_task_factory', False):
        return
    existing_factory = loop.get_task_factory()
    def task_factory(loop, coro):
        try:
            parent_task = asyncio.current_task()
        except RuntimeError:
            parent_task = None
        if existing_factory:
            task = existing_factory(loop, coro)
        else:
            task = asyncio.Task(coro, loop=loop)
        task.parent_task = parent_task
        return task
    loop.set_task_factory(task_factory)
    loop._has_panel_task_factory = True

#---------------------------------------------------------------------
# Public API
#---------------------------------------------------------------------

def serve(
    panels: 'TViewableOrFunc' | Mapping[str, 'TViewableOrFunc'], port: int = 0,
    address: Optional[str] = None, websocket_origin: Optional[str | list[str]] = None,
    loop: Optional[IOLoop] = None, show: bool = True, start: bool = True,
    title: Optional[str] = None, verbose: bool = True, location: bool = True,
    threaded: bool = False, **kwargs
) -> threading.Thread | Server:
    """
    Allows serving one or more panel objects on a single server.
    The panels argument should be either a Panel object or a function
    returning a Panel object or a dictionary of these two. If a
    dictionary is supplied the keys represent the slugs at which
    each app is served, e.g. `serve({'app': panel1, 'app2': panel2})`
    will serve apps at /app and /app2 on the server.

    Reference: https://panel.holoviz.org/user_guide/Deploy_and_Export.html#serving-multiple-apps

    Arguments
    ---------
    panel: Viewable, function or {str: Viewable or function}
      A Panel object, a function returning a Panel object or a
      dictionary mapping from the URL slug to either.
    port: int (optional, default=0)
      Allows specifying a specific port
    address : str
      The address the server should listen on for HTTP requests.
    websocket_origin: str or list(str) (optional)
      A list of hosts that can connect to the websocket.

      This is typically required when embedding a server app in
      an external web site.

      If None, "localhost" is used.
    loop : tornado.ioloop.IOLoop (optional, default=IOLoop.current())
      The tornado IOLoop to run the Server on
    show : boolean (optional, default=True)
      Whether to open the server in a new browser tab on start
    start : boolean(optional, default=True)
      Whether to start the Server
    title: str or {str: str} (optional, default=None)
      An HTML title for the application or a dictionary mapping
      from the URL slug to a customized title
    verbose: boolean (optional, default=True)
      Whether to print the address and port
    location : boolean or panel.io.location.Location
      Whether to create a Location component to observe and
      set the URL location.
    threaded: boolean (default=False)
      Whether to start the server on a new Thread
    kwargs: dict
      Additional keyword arguments to pass to Server instance
    """
    kwargs = dict(kwargs, **dict(
        port=port, address=address, websocket_origin=websocket_origin,
        loop=loop, show=show, start=start, title=title, verbose=verbose,
        location=location
    ))
    if threaded:
        kwargs['loop'] = loop = IOLoop() if loop is None else loop
        server = StoppableThread(
            target=get_server, io_loop=loop, args=(panels,), kwargs=kwargs
        )
        server_id = kwargs.get('server_id', uuid.uuid4().hex)
        state._threads[server_id] = server
        server.start()
    else:
        return get_server(panels, **kwargs)
    return server


class ProxyFallbackHandler(RequestHandler):
    """A `RequestHandler` that wraps another HTTP server callback and
    proxies the subpath.
    """

    def initialize(self, fallback, proxy=None):
        self.fallback = fallback
        self.proxy = proxy

    def prepare(self):
        if self.proxy:
            self.request.path = self.request.path.replace(self.proxy, '')
        self.fallback(self.request)
        self._finished = True
        self.on_finish()


def get_static_routes(static_dirs):
    """
    Returns a list of tornado routes of StaticFileHandlers given a
    dictionary of slugs and file paths to serve.
    """
    patterns = []
    for slug, path in static_dirs.items():
        if not slug.startswith('/'):
            slug = '/' + slug
        if slug == '/static':
            raise ValueError("Static file route may not use /static "
                             "this is reserved for internal use.")
        path = fullpath(path)
        if not os.path.isdir(path):
            raise ValueError("Cannot serve non-existent path %s" % path)
        patterns.append(
            (r"%s/(.*)" % slug, StaticFileHandler, {"path": path})
        )
    patterns.append((
        f'/{COMPONENT_PATH}(.*)', ComponentResourceHandler, {}
    ))
    return patterns

def get_server(
    panel: 'TViewableOrFunc' | Mapping[str, 'TViewableOrFunc'], port: int = 0,
    address: Optional[str] = None, websocket_origin: Optional[str | list[str]] = None,
    loop: Optional[IOLoop] = None, show: bool = False, start: bool = False,
    title: bool = None, verbose: bool = False, location: bool | Location = True,
    static_dirs: Mapping[str, str] = {}, oauth_provider: Optional[str] = None,
    oauth_key: Optional[str] = None, oauth_secret: Optional[str] = None,
    oauth_extra_params: Mapping[str, str] = {}, cookie_secret: Optional[str] = None,
    oauth_encryption_key: Optional[str] = None, session_history: Optional[int] = None,
    **kwargs
) -> Server:
    """
    Returns a Server instance with this panel attached as the root
    app.

    Arguments
    ---------
    panel: Viewable, function or {str: Viewable}
      A Panel object, a function returning a Panel object or a
      dictionary mapping from the URL slug to either.
    port: int (optional, default=0)
      Allows specifying a specific port
    address : str
      The address the server should listen on for HTTP requests.
    websocket_origin: str or list(str) (optional)
      A list of hosts that can connect to the websocket.

      This is typically required when embedding a server app in
      an external web site.

      If None, "localhost" is used.
    loop : tornado.ioloop.IOLoop (optional, default=IOLoop.current())
      The tornado IOLoop to run the Server on.
    show : boolean (optional, default=False)
      Whether to open the server in a new browser tab on start.
    start : boolean(optional, default=False)
      Whether to start the Server.
    title : str or {str: str} (optional, default=None)
      An HTML title for the application or a dictionary mapping
      from the URL slug to a customized title.
    verbose: boolean (optional, default=False)
      Whether to report the address and port.
    location : boolean or panel.io.location.Location
      Whether to create a Location component to observe and
      set the URL location.
    static_dirs: dict (optional, default={})
      A dictionary of routes and local paths to serve as static file
      directories on those routes.
    oauth_provider: str
      One of the available OAuth providers
    oauth_key: str (optional, default=None)
      The public OAuth identifier
    oauth_secret: str (optional, default=None)
      The client secret for the OAuth provider
    oauth_extra_params: dict (optional, default={})
      Additional information for the OAuth provider
    cookie_secret: str (optional, default=None)
      A random secret string to sign cookies (required for OAuth)
    oauth_encryption_key: str (optional, default=False)
      A random encryption key used for encrypting OAuth user
      information and access tokens.
    session_history: int (optional, default=None)
      The amount of session history to accumulate. If set to non-zero
      and non-None value will launch a REST endpoint at
      /rest/session_info, which returns information about the session
      history.
    kwargs: dict
      Additional keyword arguments to pass to Server instance.

    Returns
    -------
    server : panel.io.server.Server
      Bokeh Server instance running this panel
    """
    from ..config import config
    from .rest import REST_PROVIDERS

    server_id = kwargs.pop('server_id', uuid.uuid4().hex)
    kwargs['extra_patterns'] = extra_patterns = kwargs.get('extra_patterns', [])
    if isinstance(panel, dict):
        apps = {}
        for slug, app in panel.items():
            if isinstance(title, dict):
                try:
                    title_ = title[slug]
                except KeyError:
                    raise KeyError(
                        "Keys of the title dictionnary and of the apps "
                        f"dictionary must match. No {slug} key found in the "
                        "title dictionary.")
            else:
                title_ = title
            slug = slug if slug.startswith('/') else '/'+slug
            if 'flask' in sys.modules:
                from flask import Flask
                if isinstance(app, Flask):
                    wsgi = WSGIContainer(app)
                    if slug == '/':
                        raise ValueError('Flask apps must be served on a subpath.')
                    if not slug.endswith('/'):
                        slug += '/'
                    extra_patterns.append(('^'+slug+'.*', ProxyFallbackHandler,
                                           dict(fallback=wsgi, proxy=slug)))
                    continue
            if isinstance(app, pathlib.Path):
                app = str(app) # enables serving apps from Paths
            if (isinstance(app, str) and (app.endswith(".py") or app.endswith(".ipynb"))
                and os.path.isfile(app)):
                apps[slug] = build_single_handler_application(app)
            elif isinstance(app, Application):
                apps[slug] = app
            else:
                handler = FunctionHandler(partial(_eval_panel, app, server_id, title_, location))
                apps[slug] = Application(handler)
    else:
        handler = FunctionHandler(partial(_eval_panel, panel, server_id, title, location))
        apps = {'/': Application(handler)}

    extra_patterns += get_static_routes(static_dirs)

    if session_history is not None:
        config.session_history = session_history
    if config.session_history != 0:
        pattern = REST_PROVIDERS['param']([], 'rest')
        extra_patterns.extend(pattern)
        state.publish('session_info', state, ['session_info'])

    opts = dict(kwargs)
    if loop:
        loop.make_current()
        opts['io_loop'] = loop
    elif opts.get('num_procs', 1) == 1:
        opts['io_loop'] = IOLoop.current()

    if 'index' not in opts:
        opts['index'] = INDEX_HTML

    if address is not None:
        opts['address'] = address

    if websocket_origin:
        if not isinstance(websocket_origin, list):
            websocket_origin = [websocket_origin]
        opts['allow_websocket_origin'] = websocket_origin

    # Configure OAuth
    from ..config import config
    if oauth_provider:
        from ..auth import OAuthProvider
        config.oauth_provider = oauth_provider # type: ignore
        opts['auth_provider'] = OAuthProvider()
    if oauth_key:
        config.oauth_key = oauth_key # type: ignore
    if oauth_extra_params:
        config.oauth_extra_params = oauth_extra_params # type: ignore
    if cookie_secret:
        config.cookie_secret = cookie_secret # type: ignore
    opts['cookie_secret'] = config.cookie_secret

    server = Server(apps, port=port, **opts)
    if verbose:
        address = server.address or 'localhost'
        url = f"http://{address}:{server.port}{server.prefix}"
        print(f"Launching server at {url}")

    state._servers[server_id] = (server, panel, [])

    if show:
        def show_callback():
            server.show('/login' if config.oauth_provider else '/')
        server.io_loop.add_callback(show_callback)

    def sig_exit(*args, **kwargs):
        server.io_loop.add_callback_from_signal(do_stop)

    def do_stop(*args, **kwargs):
        server.io_loop.stop()

    try:
        signal.signal(signal.SIGINT, sig_exit)
    except ValueError:
        pass # Can't use signal on a thread

    if start:
        server.start()
        try:
            server.io_loop.start()
        except RuntimeError:
            pass
        except TypeError:
            warnings.warn(
                "IOLoop couldn't be started. Ensure it is started by "
                "process invoking the panel.io.server.serve."
            )
    return server


class StoppableThread(threading.Thread):
    """Thread class with a stop() method."""

    def __init__(self, io_loop: IOLoop, **kwargs):
        super().__init__(**kwargs)
        self.io_loop = io_loop

    def run(self) -> None:
        if hasattr(self, '_target'):
            target, args, kwargs = self._target, self._args, self._kwargs # type: ignore
        else:
            target, args, kwargs = self._Thread__target, self._Thread__args, self._Thread__kwargs # type: ignore
        if not target:
            return
        bokeh_server = None
        try:
            bokeh_server = target(*args, **kwargs)
        finally:
            if isinstance(bokeh_server, Server):
                try:
                    bokeh_server.stop()
                except Exception:
                    pass
            if hasattr(self, '_target'):
                del self._target, self._args, self._kwargs # type: ignore
            else:
                del self._Thread__target, self._Thread__args, self._Thread__kwargs # type: ignore

    def stop(self) -> None:
        self.io_loop.add_callback(self.io_loop.stop)
