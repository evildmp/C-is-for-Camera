c is for Camera
===============

A 35mm camera, based on the `Canonet G-III QL17 <https://en.wikipedia.org/wiki/Canonet_G-III_QL17>`_ rangefinder,
simulated in Python.

The purpose of this project is to explore and understand the logic in the mechanisms of a camera by using
object-oriented programming to simulate real-world objects.

See the `c is for Camera documentation <https://c-is-for-camera.readthedocs.io>`_.


See "Understanding Camera" below for more about *how* the camera is simulated.


Quickstart
-----------

Clone the repository::

    git clone https://github.com/evildmp/C-is-for-Camera.git

or::

    git clone git@github.com:evildmp/C-is-for-Camera.git

In the ``C-is-for-Camera`` directory, start a Python 3 shell.

::

    >>> from camera import Camera
    >>> c = Camera()
    >>> c.state()
    ================== Camera state =================

    ------------------ Mechanical -------------------
    Back closed:               True
    Lens cap on:               False
    Film advance mechanism:    False
    Shutter cocked:            False
    Shutter timer:             1/128.0 seconds
    Iris aperture:             ƒ/16
    Camera exposure settings:  15.0 EV

    ------------------ Metering ---------------------
    Light meter reading:        4096 cd/m^2
    Exposure target:            15.0 EV
    Mode:                       Shutter priority
    Battery:                    1.44 V
    Film speed:                 100 ISO

    ------------------ Environment ------------------
    Scene luminosity:           4096 cd/m^2

    >>> c.film_advance_mechanism.advance()
    Cocking shutter
    Cocked
    >>> c.shutter.trip()
    Shutter opens
    Shutter closes
    Shutter opened for 1/128 seconds
    Shutter uncocked
