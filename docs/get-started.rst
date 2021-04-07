.. _get-started:

Get started
===========

Installation
------------

You'll need Python 3.6 or later.

Clone the repository::

    git clone https://github.com/evildmp/C-is-for-Camera.git

or::

    git clone git@github.com:evildmp/C-is-for-Camera.git


Using the camera
----------------

In the ``C-is-for-Camera`` directory, start a Python 3 shell.

Now, create a ``Camera`` instance::

    >>> from camera import Camera
    >>> c = Camera()

And find out what state it's in, using the ``state()`` method::

    >>> c.state()

``state()`` reports on the state of the camera, which includes its various subsystems (which themselves are also
represented by Python classes)::

    ================== Camera state =================

    ------------------ Controls ---------------------
    Film speed:                100 ISO
    Selected speed:            1/125

    ------------------ indicators -------------------
    Light meter reading        ƒ/16
    Frame counter:             0

    ------------------ Mechanical -------------------
    Back closed:               True
    Lens cap on:               False
    Film advance mechanism:    False
    Shutter cocked:            False
    Shutter timer:             1/128 seconds
    Iris aperture:             ƒ/16
    Camera exposure settings:  Shutter priority EV

    ------------------ Metering ---------------------
    Metered light:              4096 cd/m^2
    Exposure target:            15.0 EV
    Mode:                       Shutter priority
    Battery:                    1.44 V
    Film speed:                 100 ISO

    ------------------ Film -------------------------
    Speed:                      100 ISO
    Rewound into cartridge:     False
    Exposed frames:             0 (of 24)
    Ruined:                     False

    ------------------ Environment ------------------
    Scene luminosity:           4096 cd/m^2


The lens cap is off, so let's try to take a photo. First, advance the film::

    >>> c.film_advance_lever.wind()
    On frame 0 (of 24)
    Advancing film
    On frame 1 (of 24)
    Cocking shutter
    Applying aperture value ƒ/1.7 to iris
    Cocked


As you can see, moving the lever advances the film, which also cocks the shutter. You can check ``c.state()`` again. So
now we can actually fire the shutter, by pressing the shutter release button::

    >>> c.shutter_button.press()
    Light meter reading: ƒ1/16
    Applying aperture value ƒ/16 to iris
    Shutter opening for 1/128 seconds
    Shutter closes
    Shutter uncocked

You can set the camera's speed::

    >>> c.shutter_speed = 1/250

\ - but only speeds available from the shutter speed selector ring can be set::

    >>> c.shutter_speed = 1/33
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/Users/daniele/Repositories/camera/camera.py", line 44, in shutter_speed
        raise self.NonExistentShutterSpeed(f"Possible shutter speeds are {possible_settings}")
    camera.NonExistentShutterSpeed: Possible shutter speeds are 1/4, 1/8, 1/15, 1/30, 1/60, 1/125, 1/250, 1/500

Doing other physically impossible things - like trying to wind the lever twice without taking a shot - will cause an
exception, for example::

    >>> c.film_advance_lever.wind()
    On frame 1 (of 24)
    Advancing film
    On frame 2 (of 24)
    Cocking shutter
    Applying aperture value ƒ/1.7 to iris
    Cocked
    >>> c.film_advance_lever.wind()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/Users/daniele/Repositories/camera/camera.py", line 163, in wind
        self.camera.film_advance_mechanism.advance()
      File "/Users/daniele/Repositories/camera/camera.py", line 178, in advance
        raise self.AlreadyAdvanced
    camera.AlreadyAdvanced

You can also do things that you shouldn't do, like opening the back of the camera in daylight with a partially-exposed
roll of film inside - which will spoil the film::

    >>> c.back.open()
    Opening back
    Resetting frame counter to 0
    'Film is ruined'

See :ref:`reference` for a complete description of the camera's components and what you can do with them.
