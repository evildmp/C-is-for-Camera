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

.. image:: /images/wind-film-lever.jpg
   :width: 50%
   :alt: 'Wind the film lever'

::

    c.film_advance_lever.wind()


Set a film speed setting
~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /images/set-film-speed.jpg
   :width: 100%
   :alt: 'Set the film speed'

::

    c.film_speed = <speed>

Selectable film speeds are 25, 50, 100, 200, 400, 800 ASA.


Select shutter-priority exposure mode mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /images/set-aperture-to-A.jpg
   :width: 50%
   :alt: 'Set aperture to "A"'


::

    c.aperture = "A"

Check the light meter
~~~~~~~~~~~~~~~~~~~~~~

.. image:: /images/check-exposure-indicator.jpg
   :width: 100%
   :alt: 'Check the light meter'

::

    c.exposure_indicator()

Press the shutter button
~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /images/take-photo.jpg
   :width: 100%
   :alt: 'Take a photo'

::

    c.shutter_button.press()


Set aperture manually
~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /images/set-aperture-manually.jpg
   :width: 100%
   :alt: 'Select the aperture manually'

::

    c.aperture = <ƒ-number>

Selectable ƒ-numbers are between 1.7 and 16.

Open back
~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /images/open-back.jpg
   :width: 100%
   :alt: 'Open the back of the camera'

::

    c.back.open()


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
