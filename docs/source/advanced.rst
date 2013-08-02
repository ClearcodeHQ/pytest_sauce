Advanced
========

This chapter will describe few advanced behaviours package provides

pdb - ipdb
----------

When providing --pdb option (run.pdb: true in config), pytest will drop to debug console, once error occurs within script.

But when you have pytest_ipdb installed, along with ipdb, pytest_ipdb will replace pdb for ipdb, for better debbuging experience.

To be able to use this, simply install **pytest_sauce[ipdb]** extras.

.. warning::

    pytest_ipdb provides only .egg distribution files, which pip is not able to download/install. Please use easy_install for this task, or add this to your standard setup.py requirement.
