Usage
=====

pytest_sauce does not provide tasks to run your tests (yet!), so far, this package provides methods, that run tests, but provides functions, that you can use within your pacer tasks or console scripts.

All these tasks requires is argument with yaml config location


Configuration
-------------

Package provides default configuration.

.. literalinclude:: ../../pytest_sauce/default.yaml
    :language: yaml
    :linenos:

Anything can be overriden in your test configuration.

.. note::
    You have to define separate configs for selenium and saucelabs


Browsers
++++++++

To define browsers for tests follow convention presented in pytest_mozwebqa:

https://github.com/davehunt/pytest-mozwebqa#running-tests-with-pytest_mozwebqa

Each parameter is a key in browsers list:

.. code-block: yaml

    browsers:
        -   browsername: chrome
            platform: linux
            driver: chrome

.. note::

    Mind, that for chrome you do not have to define chromedriver location, as pytest_sauce will download it anyway and pass it's path to chromepath argument to whenever you use chrome in your selenium tests.

Saucelabs
+++++++++

Saucelabs configuration should also contain these three keys:

.. code-block:: yaml

    username: <saucelabs_username>
    password: <saucelabs_password>
    api-key: <saucelabs_apikey>


It's important to have it here, as the same configuration file is passed to --saucelabs argument

xvfb
++++

selenium.xvfb is a little bit specific. you pass here xvfb-run arguments, that will configure xvfb environment. However if the whole key, will have false value, tests will be run without xvfb mode

To run test in normal mode, simply set this key to false in your config:

.. code-block:: yaml

    selenium:
        xvfb: false

.. warning::

    Previous construct is deprecated!

    .. code-block:: yaml

        selenium:
            xvfb:
                xvfb_on: false
