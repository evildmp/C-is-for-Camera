.. _how-to:

How-to guides
=============

How to operate the camera controls
-------------------------------------

All the examples below assume that you have already instantiated a ``Camera`` object::

    from camera import Camera
    c = Camera()


Advance the film
~~~~~~~~~~~~~~~~~~~~

..  rst-class:: column

::

    c.film_advance_lever.wind()

..  rst-class:: column

..  image:: /images/wind-film-lever.jpg
    :alt: 'Wind the film lever'




..  rst-class:: clearfix

Set a film speed setting
~~~~~~~~~~~~~~~~~~~~~~~~

::

    c.film_speed = <speed>

Selectable film speeds are 25, 50, 100, 200, 400, 800 ASA.

..  image:: /images/set-film-speed.jpg
   :alt: 'Set the film speed'


Select shutter-priority exposure mode mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  rst-class:: column

::

    c.aperture = "A"

..  rst-class:: column

..  image:: /images/set-aperture-to-A.jpg
    :alt: 'Set aperture to "A"'


..  rst-class:: clearfix

Check the light meter
~~~~~~~~~~~~~~~~~~~~~~

::

    c.exposure_indicator()

..  image:: /images/check-exposure-indicator.jpg
    :alt: 'Check the light meter'


Press the shutter button
~~~~~~~~~~~~~~~~~~~~~~~~

::

    c.shutter_button.press()

..  image:: /images/take-photo.jpg
    :alt: 'Take a photo'


Set aperture manually
~~~~~~~~~~~~~~~~~~~~~~~~

::

    c.aperture = <ƒ-number>

Selectable ƒ-numbers are between 1.7 and 16.

..  image:: /images/set-aperture-manually.jpg
    :alt: 'Select the aperture manually'


Open back
~~~~~~~~~~~~~~~~~~~~~~~~

::

    c.back.open()

..  image:: /images/open-back.jpg
    :alt: 'Open the back of the camera'


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
