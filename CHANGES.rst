=======
CHANGES
=======

current
-------
- xvfb_on option removed completely. Please use `xvfb: false` to disable virtual framebuffer.

0.3
-------
- upgrade Saucelab Connect to v4.3. It's not backward compatible with previous versions.

0.2.10
-------
- changed os.rename to shutil.move. Fixes moving files between partitions. [fizyk]

0.2.8
-----
- various package description improvements
- excludes buggy pymlconf requirement

0.2.6
-----
- default chromedriver version bumped to 2.2
- xvfb-run mode now starts with auto-servernum parameter by default

0.2.5
-----
- run_tests returns error code from latests test

0.2.4
-----
- public release

0.2.3
-----

- fixed xvfb turning off option
- change default option to not download Saucelabs everytime
- ability to replace pdb with ipdb

0.2.2
-----

- ability to set xvfb-run settings

0.2.0
-----

- ability to run standard py.test tests with config

0.0.0
-------
- initialize package [sliwinski]
