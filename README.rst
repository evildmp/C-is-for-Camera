c is for Camera
===============

A 35mm camera, based on the `Canonet G-III QL17 <https://en.wikipedia.org/wiki/Canonet_G-III_QL17>`_ rangefinder,
simulated in Python.

The purpose of this project is to explore and understand the logic in the mechanisms of a camera by using
object-oriented programming to simulate real-world objects.

.. image:: /docs/images/QL17.jpg
   :alt: 'Canonet G-III QL17'

It aims towards completeness in its modelling of the real world. For example, if you open the back of the camera in
daylight with a partially exposed film, it will ruin the film.

See the `c is for Camera documentation <https://c-is-for-camera.readthedocs.io>`_.


A quick tour
------------

Clone the repository::

    git clone https://github.com/evildmp/C-is-for-Camera.git

or::

    git clone git@github.com:evildmp/C-is-for-Camera.git

In the ``C-is-for-Camera`` directory, start a Python 3 shell.

::

    >>> from camera import Camera
    >>> c = Camera()

See the camera's state::

    >>> c.state()
    ================== Camera state =================

    ------------------ Mechanical -------------------
    Back closed:               True
    Lens cap on:               False
    Film advance mechanism:    False
    Frame counter:             0
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

    ------------------ Film -------------------------
    Speed:                      100 ISO
    Rewound into cartridge:     False
    Exposed frames:             0 (of 24
    Ruined:                     False

    ------------------ Environment ------------------
    Scene luminosity:           4096 cd/m^2

Advance the film::

    >>> c.film_advance_mechanism.advance()
    On frame 0 (of 24)
    Advancing film
    On frame 1 (of 24)
    Cocking shutter
    Cocked

Release the shutter::

    >>> c.shutter.trip()
    Shutter openening for 1/128 seconds
    Shutter closes
    Shutter uncocked
    'Tripped'

It's not possible to advance the mechanism twice without releasing the shutter::

    >>> c.film_advance_mechanism.advance()
    On frame 1 (of 24)
    Advancing film
    On frame 2 (of 24)
    Cocking shutter
    Cocked
    >>> c.film_advance_mechanism.advance()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/Users/daniele/Repositories/camera/camera.py", line 56, in advance
        raise self.AlreadyAdvanced
    camera.AlreadyAdvanced

If you open the back in daylight it ruins the film::

    >>> c.back.open()
    Opening back
    Resetting frame counter to 0
    'Film is ruined'

Close the back and rewind the film::

    >>> c.back.close()
    Closing back
    >>> c.film_rewind_mechanism.rewind()
    Rewinding film
