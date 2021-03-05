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

The lens cap is off, so let's try to take a photo. First, advance the film::

    >>> c.film_advance_mechanism.advance()
    Cocking shutter
    Cocked

As you can see, advancing the film also cocks the shutter. You can check ``c.state()`` again. So now we can actually
fire the shutter::

    >>> c.shutter.trip()
    Shutter opens
    Shutter closes
    Shutter opened for 1/128 seconds
    Shutter uncocked

Doing physically impossible things - like advancing the mechanism twice without releasing it - will cause an exception,
for example::

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

You can also do things that you shouldn't do, like opening the back of the camera in daylight with a partially-exposed
roll of film inside - which will spoil the film::

    >>> c.back.open()
    Opening back
    Resetting frame counter to 0
    'Film is ruined'

See :ref:`reference` for a complete description of the camera's components and what you can do with them.