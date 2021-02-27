Camera
======

A 35mm camera, simulated in Python.

Based on the Canonet G-III QL17.


Get started
-----------

Clone the repository::

    git clone https://github.com/evildmp/C-is-for-Camera.git

or::

    git clone git@github.com:evildmp/C-is-for-Camera.git

In the ``C-is-for-Camera`` directory, start a Python 3 shell.

Now, create a ``Camera`` instance::

    >>> from camera import Camera
    >>> c = Camera()

And find out what state it's in, using the ``state()`` method::

    >>> c.state()

``state()`` reports on the state of the camera, which includes its various subsystems (which themselves are also
represented Python classes)::


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


Reference
---------

Components of the camera
~~~~~~~~~~~~~~~~~~~~~~~~

* Camera

  * FilmAdvanceMechanism
  * Shutter
  * ExposureControlSystem
  * LightMeter
  * Back
  * LensCap

* Environment


Exceptions
~~~~~~~~~~

Exceptions occur when you try to do something that the camera refuses to do because itviolates the logic of a mechanism
of the camera. For example, if the shutter is already cocked, trying to call the shutter's ``cock()`` method will raise
a ``Shutter.AlreadyCocked`` exception; it's not logically possible to cock a shutter that's already cocked.

Similarly, trying to call ``FilmAdvanceMechanism.advance()`` when the mechanism is already advanced raises a
``FilmAdvanceMechanism.AlreadyAdvanced`` exception.

On the other hand, attempting to call ``Shutter.trip()`` when the shutter is not cocked simply does nothing. It doesn't
violate the logic, it just doesn't have any effect.


Why?
----

I love film cameras and their mechanisms, and spend a lot of time repairing and servicing them. The mechanisms in a
camera are full of functional logic, and thinking about how they change their own state and trigger changes in and
depend on the mechanisms they are connected to is the same kind of thinking that goes on in object-oriented programming.

This project is an experiement in expressing the logic of a camera - in this case, a `Canonet G-III QL17
<https://en.wikipedia.org/wiki/Canonet_G-III_QL17>`_ rangefinder, one of my favourites - in code.
