# Releases 

## Version 0.9.7

The 0.9.6 release unfortunately caused a major regression in layout performance due to the way optimizations in Bokeh and Panel interacted. This release fixes this regression.

- Fix regression in layout performance ([#1453](https://github.com/holoviz/panel/pull/1453))

## Version 0.9.6

This is a minor bug fix release primarily for compatibility with Bokeh versions >=2.1.0 along with a variety of important bug fixes. Many thanks for the many people who contributed to this release including @mattpap, @kebowen730, @xavArtley, @maximlt, @jbednar, @mycarta, @basnijholt, @jbednar and @philippjfr.

- Compatibility with Bokeh 2.1 ([#1424](https://github.com/holoviz/panel/pull/1424), [#1428](https://github.com/holoviz/panel/pull/1428))
- Fixes for `FileDownload` widget handling of callbacks ([#1246](https://github.com/holoviz/panel/pull/1246), [#1306](https://github.com/holoviz/panel/pull/1306))
- Improvements and fixes for Param pane widget mapping ([#1301](https://github.com/holoviz/panel/pull/1301), [#1342](https://github.com/holoviz/panel/pull/1342), [#1378](https://github.com/holoviz/panel/pull/1378)) 
- Fixed bugs handling of closed Tabs ([#1337](https://github.com/holoviz/panel/pull/1337))
- Fix bug in layout `clone` method ([#1349](https://github.com/holoviz/panel/pull/1349))
- Improvements for `Player` widget ([#1353](https://github.com/holoviz/panel/pull/1353), [#1360](https://github.com/holoviz/panel/pull/1360))
- Fix for `jslink` on Bokeh models ([#1358](https://github.com/holoviz/panel/pull/1358))
- Fix for rendering geometries in `Vega` pane ([#1359](https://github.com/holoviz/panel/pull/1359))
- Fix issue with `HoloViews` pane overriding selected renderer ([#1429](https://github.com/holoviz/panel/pull/1429))
- Fix issues with `JSON` pane depth parameter and rerendering ([#1431](https://github.com/holoviz/panel/pull/1431))
- Fixed `param.Date` and `param.CalenderDate` parameter mappings ([#1433](https://github.com/holoviz/panel/pull/1433), [#1434](https://github.com/holoviz/panel/pull/1434))
- Fixed issue with enabling `num_procs` on `pn.serve` ([#1436](https://github.com/holoviz/panel/pull/1436))
- Warn if a particular extension could not be loaded ([#1437](https://github.com/holoviz/panel/pull/1437))
- Fix issues with garbage collection and potential memory leaks ([#1407](https://github.com/holoviz/panel/pull/1407))
- Support recent versions of pydeck in `DeckGL` pane ([#1443](https://github.com/holoviz/panel/pull/1443))
- Ensure JS callbacks on widget created from Parameters are initialized ([#1439](https://github.com/holoviz/panel/pull/1439))

## Version 0.9.5

Date: 2019-04-04

This release primarily focused on improvements and additions to the documentation. Many thanks to @MarcSkovMadsen, @philippjfr and @michaelaye for contributing to this release.

Enhancements:

- Add `Template.save` with ability to save to HTML and PNG but not embed ([#1224](https://github.com/holoviz/panel/pull/1224))

Bug fixes:

- Fixed formatting of datetimes in `DataFrame` widget ([#1221](https://github.com/holoviz/panel/pull/1221))
- Add `panel/models/vtk/` subpackage to MANIFEST to ensure it is shipped with packages

Documentation:

- Add guidance about developing custom models ([#1220](https://github.com/holoviz/panel/pull/1220))
- Add Folium example to gallery ([#1189](https://github.com/holoviz/panel/pull/1189))
- Add `FileDownload` and `FileInput` example to gallery ([#1193](https://github.com/holoviz/panel/pull/1193))

## Version 0.9.4

Date: 2020-04-02

This is a minor release fixing a number of regressions and compatibility issues which continue to crop up due to the upgrade to Bokeh 2.0 Additionally this release completely overhauls how communication in notebook environments are handled, eliminating the need to register custom callbacks with inlined JS callbacks to sync properties. Many thanks to the contributors to this release including @hyamanieu, @maximlt, @mattpap and the maintainer @philippjfr.

Enhancements:

- Switch to using CommManager in notebook hugely simplifying comms in notebooks and reducing the amount of inlined Javascript ([#1171](https://github.com/holoviz/panel/pull/1171))
- Add ability to serve Flask apps directly using pn.serve ([#1215](https://github.com/holoviz/panel/pull/1215)) 

Bug fixes:

- Fix bug in Template which caused all roots to instantiate two models for each component ([#1216](https://github.com/holoviz/panel/pull/1216))
- Fixed bug with Bokeh 2.0 DataPicker datetime format ([#1187](https://github.com/holoviz/panel/pull/1187))
- Publish Panel.js to CDN to allow static HTML exports with CDN resources to work ([#1190](https://github.com/holoviz/panel/pull/1190))
- Handle bug in rendering Vega models with singular dataset ([#1201](https://github.com/holoviz/panel/pull/1201))
- Removed escaping workaround for HTML models resulting in broken static exports ([#1206](https://github.com/holoviz/panel/pull/1206))
- Fixed bug closing Tabs ([#1208](https://github.com/holoviz/panel/pull/1208))
- Embed Panel logo in server index.html ([#1209](https://github.com/holoviz/panel/pull/1209))

Compatibility:

- This release adds compatibility with Bokeh 2.0.1 which caused a regression in loading custom models

## Version 0.9.3

Date: 2019-03-21

This is a minor release fixing an issue with recent versions of Tornado. It also fixes issue with the packages built on the PyViz conda channel.

- Respect write-locks on synchronous Websocket events (#1170)

## Version 0.9.2

Date: 2019-03-21

This is a minor release with a number of bug fixes. Many thanks to @ceball, @Guillemdb and @philippjfr for contributing these fixes.

Bug fixes:

- Fix regression in DiscreteSlider layout (#1163)
- Fix for saving as PNG which regressed due to changes in bokeh 2.0 (#1165)
- Allow pn.serve to resolve Template instances returned by a function (#1167)
- Ensure Template can render empty HoloViews pane (#1168)

## Version 0.9.1

Date: 2019-03-19

This is very minor releases fixing small regressions in the 0.9.0 release:

Bug fixes:

- Fix issue with `Button` label not being applied (#1152)
- Pin pyviz_comms 0.7.4 to avoid issues with undefined vars (#1153)

## Version 0.9.0

Date: 2019-03-13

This is a major release primarily for compatibility with the recent Bokeh 2.0 release. Additionally this release has a small number of features and bug fixes:

Features:

- Added a `MultiChoice` widget (#1140)
- Add `FileDownload` widget (#915, #1146)
- Add ability to define `Slider` format option (#1142)
- Expose `pn.state.cookies` and `pn.state.headers` to allow accessing HTTP headers and requests from inside an app (#1143)

Bug fixes:

- Ensure `DiscreteSlider` respects layout options (#1144)

Removals:

- Slider no longer support `callback_policy` and `callback_throttle` as they have been replaced by the `value_throttled` property in bokeh

## Version 0.8.1

Date: 2019-03-11

This release is a minor release with a number of bug fixes and minor enhancements. Many thanks to the community of contributors including @bstadlbauer, @ltalirz @ceball and @gmoutsofor submitting the fixes and the maintainers, including @xavArtley, @jbednar and @philippjfr, for continued development.

Minor enhancements:

- Added verbose option to display server address (#1098) [@philippjfr]

Bug fixes:

- Fix PNG export due to issue with PhantomJS (#1081, #1092) [@bstadlbauer, @philippjfr]
- Fix for threaded server (#1090) [@xavArtley]
- Ensure Plotly Pane does not perform rerender on each property change (#1109) [@philippjfr]
- Fix issues with jslink and other callbacks in Template (#1135) [@philippjfr]
- Various fixes for VTK pane (#1123) [@xavArtley]
- Fixes for .show keyword arguments (#1073, #1106) [@gmoutso]

## Version 0.8.0

Date: 2019-01-31

This release focuses primarily on solidifying existing functionality, significantly improving performance and fixing a number of important bugs. Additionally this release contains exciting new functionality, including several new components.  We want to thank the many contributors to this release (a full list is provided at the bottom), particularly @MarcSkovMadsen (the author of [awesome-panel.org](http://awesome-panel.org)) and @xavArtley, who has been hard at work at improving VTK support. We also want to thank the remaining contributors including @philippjfr, @ceball, @jbednar, @jlstevens, @Italirz, @mattpap, @Jacob-Barhak, @stefjunod and @kgullikson88. This release required only minimal changes in existing APIs and added a small number of new ones, reflecting the fact that Panel is now relatively stable and is progressing steadily towards a 1.0 release.

### Major Features & Enhancements

- Added new `DeckGL` pane ([#1019](https://github.com/holoviz/panel/issues/1019), [#1027](https://github.com/holoviz/panel/issues/1027))
- Major improvements to support for JS linking ([#1007](https://github.com/holoviz/panel/issues/1007))
- Huge performance improvements when nesting a lot of components deeply ([#867](https://github.com/holoviz/panel/issues/867), [#888](https://github.com/holoviz/panel/issues/888), [#895](https://github.com/holoviz/panel/issues/895), [#988](https://github.com/holoviz/panel/issues/988))
- Add support for displaying callback errors and print output in the notebook simplifying debugging ([#977](https://github.com/holoviz/panel/issues/977))
- Add support for dynamically populating `Tabs` ([#995](https://github.com/holoviz/panel/issues/995))
- Added `FileSelector` widget to browse the servers file system and select files ([#909](https://github.com/holoviz/panel/issues/909))
- Add `pn.serve` function to serve multiple apps at once on the same serve ([#963](https://github.com/holoviz/panel/issues/963))
- Add a `JSON` pane to display json data in a tree format ([#953](https://github.com/holoviz/panel/issues/953))

### Enhancements

- Updated Parameter mappings ([#999](https://github.com/holoviz/panel/issues/999))
- Ensure that closed tabs update `Tabs.objects` ([#973](https://github.com/holoviz/panel/issues/973))
- Fixed HoloViews axis linking across `Template` roots ([#980](https://github.com/holoviz/panel/issues/980))
- Merge FactorRange when linking HoloViews axes ([#968](https://github.com/holoviz/panel/issues/968))
- Expose title and other kwargs on `.show()` ([#962](https://github.com/holoviz/panel/issues/962))
- Let `FileInput` widget set filename ([#956](https://github.com/holoviz/panel/issues/956)
- Expose further bokeh CLI commands and added help ([#951](https://github.com/holoviz/panel/issues/951))
- Enable responsive sizing for `Vega`/altair pane ([#949](https://github.com/holoviz/panel/issues/949))
- Added encode parameter to `SVG` pane ([#913](https://github.com/holoviz/panel/issues/913))
- Improve `Markdown` handling including syntax highlighting and indentation ([#881](https://github.com/holoviz/panel/issues/881))
- Add ability to define Template variables ([#815](https://github.com/holoviz/panel/issues/815))
- Allow configuring responsive behavior globally ([#851](https://github.com/holoviz/panel/issues/851))
- Ensure that changes applied in callbacks are reflected on the frontend immediately ([#857](https://github.com/holoviz/panel/issues/857))
- Add ability to add axes coordinates to `VTK` view ([#817](https://github.com/holoviz/panel/issues/817))
- Add config option for `safe_embed` which ensures all state is recorded ([#1040](https://github.com/holoviz/panel/issues/1040))
- Implemented `__signature__` for tab completion ([#1029](https://github.com/holoviz/panel/issues/1029))

### Bug fixes

- Fixed `DataFrame` widget selection parameter ([#989](https://github.com/holoviz/panel/issues/989))
- Fixes for rendering long strings on Windows systems ([#986](https://github.com/holoviz/panel/issues/986))
- Ensure that panel does not modify user objects ([#967](https://github.com/holoviz/panel/issues/967))
- Fix multi-level expand `Param` subobject ([#965](https://github.com/holoviz/panel/issues/965))
- Ensure `load_notebook` is executed only once ([#1000](https://github.com/holoviz/panel/issues/1000))
- Fixed bug updating `StaticText` on server ([#964](https://github.com/holoviz/panel/issues/964))
- Do not link `HoloViews` axes with different types ([#937](https://github.com/holoviz/panel/issues/937))
- Ensure that integer sliders are actually integers ([#876](https://github.com/holoviz/panel/issues/876))
- Ensure that `GridBox` contents maintain size ([#971](https://github.com/holoviz/panel/issues/971))

### Compatibility

- Compatibility for new Param API ([#992](https://github.com/holoviz/panel/issues/992), [#998](https://github.com/holoviz/panel/issues/998))
- Changes for compatibility with Vega5 and altair 4 ([#873](https://github.com/holoviz/panel/issues/873), [#889](https://github.com/holoviz/panel/issues/889), [#892](https://github.com/holoviz/panel/issues/892), [#927](https://github.com/holoviz/panel/issues/927), [#933](https://github.com/holoviz/panel/issues/933))

### Backwards compatibility

- The Ace pane has been deprecated in favor of the Ace widget ([#908](https://github.com/holoviz/panel/issues/908))

### Docs

- Updated Django multiple app example and user guide ([#928](https://github.com/holoviz/panel/issues/928)) [@stefjunod]
- Clarify developer installation instructions, and fix up some metadata. ([#952](https://github.com/holoviz/panel/issues/952), [#978](https://github.com/holoviz/panel/issues/978))
- Added `Param` reference notebook ([#944](https://github.com/holoviz/panel/issues/944))
- Added `Divider` reference notebook

## Version 0.7.0

Date: 2019-11-18T21:22:16Z

This major release includes significant new functionality along with important bug and documentation fixes, including contributions from @philippjfr (maintainer and lead developer), @xavArtley (VTK support), @jbednar (docs), @DancingQuanta (FileInput), @a-recknagel (Python 3.8 support, misc), @julwin (TextAreaInput, PasswordInput), @rs2 (example notebooks), @xtaje (default values), @Karamya (Audio widget), @ceball, @ahuang11 , @eddienko, @Jacob-Barhak, @jlstevens, @jsignell, @kleavor, @lsetiawan, @mattpap, @maxibor, and @RedBeardCode.

Major enhancements:d
- Added pn.ipywidget() function for using panels and panes as ipwidgets, e.g. in voila ([#745](https://github.com/holoviz/panel/issues/745), [#755](https://github.com/holoviz/panel/issues/755), [#771](https://github.com/holoviz/panel/issues/771))
- Greatly expanded and improved Pipeline, which now allows branching graphs ([#712](https://github.com/holoviz/panel/issues/712), [#735](https://github.com/holoviz/panel/issues/735), [#737](https://github.com/holoviz/panel/issues/737), [#770](https://github.com/holoviz/panel/issues/770))
- Added streaming helper objects, including for the streamz package ([#767](https://github.com/holoviz/panel/issues/767), [#769](https://github.com/holoviz/panel/issues/769))
- Added VTK gallery example and other VTK enhancements ([#605](https://github.com/holoviz/panel/issues/605), [#606](https://github.com/holoviz/panel/issues/606), [#715](https://github.com/holoviz/panel/issues/715), [#729](https://github.com/holoviz/panel/issues/729))
- Add GridBox layout ([#608](https://github.com/holoviz/panel/issues/608), [#761](https://github.com/holoviz/panel/issues/761), [#763](https://github.com/holoviz/panel/issues/763))
- New widgets and panes:
   * Progress bar ([#726](https://github.com/holoviz/panel/issues/726))
   * Video ([#696](https://github.com/holoviz/panel/issues/696))
   * TextAreaInput widget ([#658](https://github.com/holoviz/panel/issues/658))
   * PasswordInput widget ([#655](https://github.com/holoviz/panel/issues/655))
   * Divider ([#756](https://github.com/holoviz/panel/issues/756)),
   * bi-directional jslink ([#764](https://github.com/holoviz/panel/issues/764))
   * interactive DataFrame pane for Pandas, Dask and Streamz dataframes ([#560](https://github.com/holoviz/panel/issues/560), [#751](https://github.com/holoviz/panel/issues/751))

Other enhancements:
- Make Row/Column scrollable ([#760](https://github.com/holoviz/panel/issues/760))
- Support file-like objects (not just paths) for images ([#686](https://github.com/holoviz/panel/issues/686))
- Added isdatetime utility ([#687](https://github.com/holoviz/panel/issues/687))
- Added repr, kill_all_servers, and cache to pn.state ([#697](https://github.com/holoviz/panel/issues/697),[#776](https://github.com/holoviz/panel/issues/776))
- Added Slider value_throttled parameter ([#777](https://github.com/holoviz/panel/issues/777))
- Extended existing widgets and panes:
   * WidgetBox can be disabled programmatically ([#532](https://github.com/holoviz/panel/issues/532))
   * Templates can now render inside a notebook cell ([#666](https://github.com/holoviz/panel/issues/666))
   * Added jscallback method to Viewable objects ([#665](https://github.com/holoviz/panel/issues/665))
   * Added min_characters parameter to AutocompleteInput ([#721](https://github.com/holoviz/panel/issues/721))
   * Added accept parameter to FileInput ([#602](https://github.com/holoviz/panel/issues/602))
   * Added definition_order parameter to CrossSelector ([#570](https://github.com/holoviz/panel/issues/570))
   * Misc widget fixes and improvements ([#703](https://github.com/holoviz/panel/issues/703), [#717](https://github.com/holoviz/panel/issues/717), [#724](https://github.com/holoviz/panel/issues/724), [#762](https://github.com/holoviz/panel/issues/762), [[#775](https://github.com/holoviz/panel/issues/775)](https://github.com/holoviz/panel/issues/775))

Bug fixes and minor improvements:
- Removed mutable default args ([#692](https://github.com/holoviz/panel/issues/692), [#694](https://github.com/holoviz/panel/issues/694))
- Improved tests ([#691](https://github.com/holoviz/panel/issues/691), [#699](https://github.com/holoviz/panel/issues/699), [#700](https://github.com/holoviz/panel/issues/700))
- Improved fancy layout for scrubber ([#571](https://github.com/holoviz/panel/issues/571))
- Improved plotly datetime handling ([#688](https://github.com/holoviz/panel/issues/688), [#698](https://github.com/holoviz/panel/issues/698))
- Improved JSON embedding ([#589](https://github.com/holoviz/panel/issues/589))
- Misc fixes and improvements ([#626](https://github.com/holoviz/panel/issues/626), [#631](https://github.com/holoviz/panel/issues/631), [#645](https://github.com/holoviz/panel/issues/645), [#662](https://github.com/holoviz/panel/issues/662), [#681](https://github.com/holoviz/panel/issues/681), [#689](https://github.com/holoviz/panel/issues/689), [#695](https://github.com/holoviz/panel/issues/695), [#723](https://github.com/holoviz/panel/issues/723), [#725](https://github.com/holoviz/panel/issues/725), [#738](https://github.com/holoviz/panel/issues/738), [#743](https://github.com/holoviz/panel/issues/743), [#744](https://github.com/holoviz/panel/issues/744), [#748](https://github.com/holoviz/panel/issues/748), [#749](https://github.com/holoviz/panel/issues/749), [#758](https://github.com/holoviz/panel/issues/758), [#768](https://github.com/holoviz/panel/issues/768), [#772](https://github.com/holoviz/panel/issues/772), [#774](https://github.com/holoviz/panel/issues/774), [[#775](https://github.com/holoviz/panel/issues/775)](https://github.com/holoviz/panel/issues/775), [#779](https://github.com/holoviz/panel/issues/779), [#784](https://github.com/holoviz/panel/issues/784), [#785](https://github.com/holoviz/panel/issues/785), [#787](https://github.com/holoviz/panel/issues/787), [#788](https://github.com/holoviz/panel/issues/788), [#789](https://github.com/holoviz/panel/issues/789))
- Prepare support for python 3.8 ([#702](https://github.com/holoviz/panel/issues/702))

Documentation:
- Expanded and updated FAQ ([#750](https://github.com/holoviz/panel/issues/750), [#765](https://github.com/holoviz/panel/issues/765))
- Add Comparisons section ([#643](https://github.com/holoviz/panel/issues/643))
- Docs fixes and improvements ([#635](https://github.com/holoviz/panel/issues/635), [#670](https://github.com/holoviz/panel/issues/670), [#705](https://github.com/holoviz/panel/issues/705), [#708](https://github.com/holoviz/panel/issues/708), [#709](https://github.com/holoviz/panel/issues/709), [#740](https://github.com/holoviz/panel/issues/740), [#747](https://github.com/holoviz/panel/issues/747), [#752](https://github.com/holoviz/panel/issues/752))

## Version 0.6.2

Date: 2019-08-08T15:13:31Z

Minor bugfix release patching issues with 0.6.1, primarily in the CI setup. Also removed the not-yet-supported definition_order parameter of pn.CrossSelector.

## Version 0.6.4

Date: 2019-10-08T17:41:51Z

This release includes a number of important bug fixes along with some minor enhancements, including contributions from @philippjfr, @jsignell, @ahuang11, @jonmmease, and @hoseppan.

Enhancements:

- Allow pn.depends and pn.interact to accept widgets and update their output when widget values change ([#639](https://github.com/holoviz/panel/issues/639))
- Add fancy_layout option to HoloViews pane ([#543](https://github.com/holoviz/panel/issues/543))
- Allow not embedding local files (e.g. images) when exporting to HTML ([#625](https://github.com/holoviz/panel/issues/625))

Bug fixes and minor improvements:

- Restore logging messages that were being suppressed by the distributed package ([#682](https://github.com/holoviz/panel/issues/682))
- HoloViews fixes and improvements ([#595](https://github.com/holoviz/panel/issues/595), [#599](https://github.com/holoviz/panel/issues/599), [#601](https://github.com/holoviz/panel/issues/601), [#659](https://github.com/holoviz/panel/issues/659))
- Misc other bug fixes and improvements ([#575](https://github.com/holoviz/panel/issues/575), [#588](https://github.com/holoviz/panel/issues/588), [#649](https://github.com/holoviz/panel/issues/649), [#654](https://github.com/holoviz/panel/issues/654), [#657](https://github.com/holoviz/panel/issues/657), [#660](https://github.com/holoviz/panel/issues/660), [#667](https://github.com/holoviz/panel/issues/667), [#677](https://github.com/holoviz/panel/issues/677))

Documentation:
- Added example of opening a URL from jslink ([#607](https://github.com/holoviz/panel/issues/607))


## Version 0.6.3

Date: 2019-09-19T10:28:36Z

This release saw a number of important bug and documentation fixes along with some minor enhancements.

Enhancements:

- Added support for embedding Player widget ([#584](https://github.com/holoviz/panel/issues/584))
- Add support for linking HoloViews plot axes across panels ([#586](https://github.com/holoviz/panel/issues/586))
- Allow saving to BytesIO buffer ([#596](https://github.com/holoviz/panel/issues/596)) 
- Allow `PeriodicCallback.period` to be updated dynamically ([#609](https://github.com/holoviz/panel/issues/609)) 

Bug fixes:

- While hooks are applied to model no events are sent to frontend ([#585](https://github.com/holoviz/panel/issues/585))
- Various fixes for embedding and rendering ([#594](https://github.com/holoviz/panel/issues/594))

Documentation:

- New example of periodic callbacks ([#573](https://github.com/holoviz/panel/issues/573))
- Improve `panel serve` documentation ([#611](https://github.com/holoviz/panel/issues/611), [#614](https://github.com/holoviz/panel/issues/614))
- Add server deployment guide ([#642](https://github.com/holoviz/panel/issues/642))

## Version 0.6.1

Date: 2019-08-01T14:54:20Z

## Version 0.6.0

Date: 2019-06-02T17:56:26Z

## Version 0.5.1

Date: 2019-04-11T16:52:06Z

Minor release closely following up on 0.5.0 updating version requirements to include the officially released bokeh 1.1.0. This release also includes contributions from @philippjfr (with fixes for pipeline and embed features), @xavArtley (addition of a new widget) and @banesullivan (fixes for VTK support).

Features:

- Addition of ``Spinner`` widget for numeric inputs ([#368](https://github.com/holoviz/panel/issues/368))

Bugfixes:

- Skip jslinked widgets when using embed ([#376](https://github.com/holoviz/panel/issues/376))
- Correctly revert changes to pipelines when stage transitions fail ([#375](https://github.com/holoviz/panel/issues/375))
- Fixed bug handling scalar arrays in VTK pane ([#372](https://github.com/holoviz/panel/issues/372))

## Version 0.5.0

Date: 2019-04-04T00:42:59Z

Major new release, greatly improving usability and capabilities.  Includes contributions from  @philippjfr (docs, better layouts, and many other features),  @xavArtley (VTK support, Ace code editor), @banesullivan (VTK support),  @jbednar and @rtmatx (docs),  @jsignell (docs, infrastructure, interact support), and @jlstevens (labels for parameters).

Major new features:

- Now uses Bokeh 1.1's greatly improved layout system, requiring far fewer manual adjustments to spacing ([#32](https://github.com/holoviz/panel/issues/32))
- Greatly expanded docs, now with galleries ([#241](https://github.com/holoviz/panel/issues/241), [#251](https://github.com/holoviz/panel/issues/251), [#265](https://github.com/holoviz/panel/issues/265), [#281](https://github.com/holoviz/panel/issues/281), [#318](https://github.com/holoviz/panel/issues/318), [#332](https://github.com/holoviz/panel/issues/332), [#347](https://github.com/holoviz/panel/issues/347), [#340](https://github.com/holoviz/panel/issues/340))
- Allow embedding app state, to support static HTML export of panels ([#250](https://github.com/holoviz/panel/issues/250))
- Added new GridSpec layout type, making it simpler to make grid-based dashboards ([#338](https://github.com/holoviz/panel/issues/338))
- Added VTK 3D object pane ([#312](https://github.com/holoviz/panel/issues/312), [#337](https://github.com/holoviz/panel/issues/337), [#349](https://github.com/holoviz/panel/issues/349), [#355](https://github.com/holoviz/panel/issues/355), [#363](https://github.com/holoviz/panel/issues/363))
- Added Ace code editor pane ([#359](https://github.com/holoviz/panel/issues/359))
- Allow defining external JS and CSS resources via config, making it easier to extend Panel ([#330](https://github.com/holoviz/panel/issues/330))
- Add HTML model capable of executing JS code, allowing more complex embedded items ([#32](https://github.com/holoviz/panel/issues/32)6)
- Add a KaTeX and MathJax based LaTeX pane, replacing the previous limited matplotlib/PNG-based support ([#311](https://github.com/holoviz/panel/issues/311))

Other new features:

- Allow passing Parameter instances to Param pane, making it much simpler to work with individual parameters ([#303](https://github.com/holoviz/panel/issues/303))
- Added parameter for widget alignment ([#367](https://github.com/holoviz/panel/issues/367))
- Allow specifying initial value when specifying min/max/step for interact ([#334](https://github.com/holoviz/panel/issues/334))
- Add support for param.Number step ([#365](https://github.com/holoviz/panel/issues/365))
- Add a PeriodicCallback ([#348](https://github.com/holoviz/panel/issues/348))
- Expose curdoc and session_context when using serve ([#336](https://github.com/holoviz/panel/issues/336))
- Add support for saving and loading embedded data from JSON ([#301](https://github.com/holoviz/panel/issues/301))
- Add support for specifying arbitrary `label` for Parameters ([#290](https://github.com/holoviz/panel/issues/290))
- Add ColorPicker widget ([#267](https://github.com/holoviz/panel/issues/267))
- Add support for interact title ([#266](https://github.com/holoviz/panel/issues/266))

Bugfixes and minor improvements:

- Combine HTML and JS in MIME bundle to improve browser compatibility ([#32](https://github.com/holoviz/panel/issues/32)7)
- Inlined subobject expand toggle button ([#32](https://github.com/holoviz/panel/issues/32)9)
- Use Select widget for ObjectSelector consistently to avoid issues with short lists and numeric lists ([#362](https://github.com/holoviz/panel/issues/362))
- Various small improvements ([#238](https://github.com/holoviz/panel/issues/238), [#245](https://github.com/holoviz/panel/issues/245), [#257](https://github.com/holoviz/panel/issues/257), [#258](https://github.com/holoviz/panel/issues/258), [#259](https://github.com/holoviz/panel/issues/259), [#262](https://github.com/holoviz/panel/issues/262), [#264](https://github.com/holoviz/panel/issues/264), [#276](https://github.com/holoviz/panel/issues/276), [#289](https://github.com/holoviz/panel/issues/289), [#293](https://github.com/holoviz/panel/issues/293), [#307](https://github.com/holoviz/panel/issues/307), [#313](https://github.com/holoviz/panel/issues/313), [#343](https://github.com/holoviz/panel/issues/343), [#331](https://github.com/holoviz/panel/issues/331))
- Various bugfixes ([#247](https://github.com/holoviz/panel/issues/247), [#261](https://github.com/holoviz/panel/issues/261), [#263](https://github.com/holoviz/panel/issues/263), [#282](https://github.com/holoviz/panel/issues/282), [#288](https://github.com/holoviz/panel/issues/288), [#291](https://github.com/holoviz/panel/issues/291), [#297](https://github.com/holoviz/panel/issues/297), [#295](https://github.com/holoviz/panel/issues/295), [#305](https://github.com/holoviz/panel/issues/305), [#309](https://github.com/holoviz/panel/issues/309), [#32](https://github.com/holoviz/panel/issues/32)2, [#32](https://github.com/holoviz/panel/issues/32)8, [#341](https://github.com/holoviz/panel/issues/341), [#345](https://github.com/holoviz/panel/issues/345), [#354](https://github.com/holoviz/panel/issues/354), [#364](https://github.com/holoviz/panel/issues/364))

Changes potentially affecting backwards compatibility:

- Refactored io subpackage ([#315](https://github.com/holoviz/panel/issues/315))
- Moved panes and widgets into subpackage ([#283](https://github.com/holoviz/panel/issues/283))
- Cleaned up wdiget, deploy, and export APIs ([#268](https://github.com/holoviz/panel/issues/268), [#269](https://github.com/holoviz/panel/issues/269))
- Renamed pane precedence to priority to avoid confusion with Param precedence ([#235](https://github.com/holoviz/panel/issues/235))


## Version 0.3.1

Date: 2018-12-05T22:49:23Z

Minor release fixing packaging issues.

## Version 0.3.0

Date: 2018-12-05T00:47:25Z

Thanks to @mhc03 for bugfixes.

New features and enhancements
- New app: Euler's Method ([#161](https://github.com/holoviz/panel/issues/161))
- New widgets and panes: Player ([#110](https://github.com/holoviz/panel/issues/110)), DiscretePlayer ([#171](https://github.com/holoviz/panel/issues/171)), CrossSelector ([#153](https://github.com/holoviz/panel/issues/153))
- Spinner (spinner.gif)
- Compositional string reprs ([#129](https://github.com/holoviz/panel/issues/129))
- Add Param.widgets parameter to override default widgets ([#172](https://github.com/holoviz/panel/issues/172))
- Pipeline improvements ([#145](https://github.com/holoviz/panel/issues/145), etc.)
- Additional entry points for user commands ([#176](https://github.com/holoviz/panel/issues/176))
- Support calling from anaconda-project ([#133](https://github.com/holoviz/panel/issues/133))
- Improved docs

Bugfixes:
- Fix example packaging ([#177](https://github.com/holoviz/panel/issues/177))
- Various bugfixes and compatibility improvements ([#126](https://github.com/holoviz/panel/issues/126), [#128](https://github.com/holoviz/panel/issues/128), [#132](https://github.com/holoviz/panel/issues/132), [#136](https://github.com/holoviz/panel/issues/136), [#141](https://github.com/holoviz/panel/issues/141), [#142](https://github.com/holoviz/panel/issues/142), [#150](https://github.com/holoviz/panel/issues/150), [#151](https://github.com/holoviz/panel/issues/151), [#154](https://github.com/holoviz/panel/issues/154), etc.)

Compatibility changes
- Renamed Param expand options ([#127](https://github.com/holoviz/panel/issues/127))


## Version 0.4.0

Date: 2019-01-28T18:02:57Z

Thanks to @xavArtley for several contributions, and to @lebedov for bugfixes.

New features:

- Now Python2 compatible ([#225](https://github.com/holoviz/panel/issues/225))
- Audio player widget ([#215](https://github.com/holoviz/panel/issues/215),[#221](https://github.com/holoviz/panel/issues/221))
- FileInput widget ([#207](https://github.com/holoviz/panel/issues/207))
- General support for linking Panel objects, even in static exports ([#199](https://github.com/holoviz/panel/issues/199))
- New user-guide notebooks: Introduction ([#178](https://github.com/holoviz/panel/issues/178)), Links ([#195](https://github.com/holoviz/panel/issues/195)).

Enhancements:
- Improved Pipeline ([#220](https://github.com/holoviz/panel/issues/220), [#222](https://github.com/holoviz/panel/issues/222))

Bug fixes:
- Windows-specific issues ([#204](https://github.com/holoviz/panel/issues/204), [#209](https://github.com/holoviz/panel/issues/209), etc.)
- Various bugfixes ([#188](https://github.com/holoviz/panel/issues/188), [#189](https://github.com/holoviz/panel/issues/189), [#190](https://github.com/holoviz/panel/issues/190), [#203](https://github.com/holoviz/panel/issues/203))


## Version 0.1.3

Date: 2018-10-23T12:09:07Z

