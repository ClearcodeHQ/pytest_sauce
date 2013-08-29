pytest_sauce
==================

`Latest documentation <https://pytest_sauce.readthedocs.org/en/latest/>`_

pytest_sauce is a pytest wrapper, that makes it easier to configure and run selenium tests both locally and on saucelabs with pytest.

It contains methods to:

- download and run saucelabs connector
- download chromedriver
- run tests on multiple browsers
- if chrome found within browser set to have tests run, checks and downloads chromedriver.

So far, this package provides only methods, that you have to use within your own tasks to run tests. But in the future, it'll provide at least one method to run tests depend on configuration file.

All these tasks requires is argument with yaml config location



.. image:: https://pypip.in/v/pytest_sauce/badge.png
    :target: https://crate.io/packages/pytest_sauce/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/pytest_sauce/badge.png
    :target: https://crate.io/packages/pytest_sauce/
    :alt: Number of PyPI downloads
