.. _how-to:

How-to guides
=============

How to run tests
----------------

Tests are in ``test_camera.py`` and require pytest.

Install pytest, and run: ``pytest``.


How to build the documentation
------------------------------

In the ``docs`` directory, run::

    make install

This creates a virtual environment and installs the components listed in ``docs/requirements.txt``.

To build the documentation, run::

    make html

The documentation can be found ``docs/_build/html``.

Or to build and serve it, with automatic refresh on changes::

    make run

The documentation is served at http://127.0.0.1:8080

To check spelling, run::

    make spelling

Any correctly spelled but unrecognised words should be added to ``docs/spelling_wordlist.txt``.
