========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |downloads| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-reaqt/badge/?style=flat
    :target: https://readthedocs.org/projects/python-reaqt
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/tmbb/python-reaqt.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/tmbb/python-reaqt

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/tmbb/python-reaqt?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/tmbb/python-reaqt

.. |requires| image:: https://requires.io/github/tmbb/python-reaqt/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/tmbb/python-reaqt/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/tmbb/python-reaqt/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/tmbb/python-reaqt

.. |version| image:: https://img.shields.io/pypi/v/reaqt.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/reaqt

.. |commits-since| image:: https://img.shields.io/github/commits-since/tmbb/python-reaqt/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/tmbb/python-reaqt/compare/v0.1.0...master

.. |downloads| image:: https://img.shields.io/pypi/dm/reaqt.svg
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/reaqt

.. |wheel| image:: https://img.shields.io/pypi/wheel/reaqt.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/reaqt

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/reaqt.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/reaqt

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/reaqt.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/reaqt


.. end-badges

2-way databiinding for Qt applications using PyRX

* Free software: BSD license

Installation
============

::

    pip install reaqt

Documentation
=============

https://python-reaqt.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
