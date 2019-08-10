***************
Getting Started
***************

Welcome to Panel!

This section will get you set up with Panel and provide a basic overview of the features and strengths of Panel. The `announcement blog <http://blog.pyviz.org/panel_announcement.html>`_ is another great resource to learn about the features of Panel and get an idea of what it can do.

Installation
------------

|CondaPyViz|_ |CondaDefaults|_ |PyPI|_ |License|_

Panel works with `Python 2.7 and Python 3 <https://travis-ci.org/pyviz/panel>`_ on Linux, Windows, or Mac.  The recommended way to install Panel is using the `conda <http://conda.pydata.org/docs/>`_ command provided by `Anaconda <http://docs.continuum.io/anaconda/install>`_ or `Miniconda <http://conda.pydata.org/miniconda.html>`_::

  conda install -c pyviz panel

or using PyPI::

  pip install panel

Support for classic Jupyter Notebook is included with Panel. If you want to work with JupyterLab, you will also need to install the optional PyViz JupyterLab extension::

  conda install -c conda-forge jupyterlab
  jupyter labextension install @pyviz/jupyterlab_pyviz


.. |CondaPyViz| image:: https://img.shields.io/conda/v/pyviz/panel.svg
.. _CondaPyViz: https://anaconda.org/pyviz/panel

.. |CondaDefaults| image:: https://img.shields.io/conda/v/anaconda/panel.svg?label=conda%7Cdefaults
.. _CondaDefaults: https://anaconda.org/anaconda/panel

.. |PyPI| image:: https://img.shields.io/pypi/v/panel.svg
.. _PyPI: https://pypi.python.org/pypi/panel

.. |License| image:: https://img.shields.io/pypi/l/panel.svg
.. _License: https://github.com/pyviz/panel/blob/master/LICENSE.txt


Using Panel
-----------

.. notebook:: panel ../../examples/getting_started/Introduction.ipynb
