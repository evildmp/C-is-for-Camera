Camera
======

A 35mm camera, based on the `Canonet G-III QL17 <https://en.wikipedia.org/wiki/Canonet_G-III_QL17>`_ rangefinder,
simulated in Python.

The purpose of this project is to explore and understand the logic in the mechanisms of a camera by using
object-oriented programming to simulate real-world objects.

See "Understanding Camera" below for more about *how* the camera is simulated.


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


How to run tests
----------------

Tests are in ``test_camera.py`` and require pytest.

Install pytest, and run: ``pytest``.


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

Exceptions occur when you try to do something that the camera refuses to do because it violates the logic of a mechanism
of the camera. For example, if the shutter is already cocked, trying to call the shutter's ``cock()`` method will raise
a ``Shutter.AlreadyCocked`` exception; it's not logically possible to cock a shutter that's already cocked.

Similarly, trying to call ``FilmAdvanceMechanism.advance()`` when the mechanism is already advanced raises a
``FilmAdvanceMechanism.AlreadyAdvanced`` exception.

On the other hand, attempting to call ``Shutter.trip()`` when the shutter is not cocked simply does nothing. It doesn't
violate the logic, it just doesn't have any effect.


Explanation
-----------

Understanding ``Camera``
~~~~~~~~~~~~~~~~~~~~~~~~

A camera is an instance of the ``Camera`` class. When a ``Camera`` is instantiated (``c = Camera()``), it's
initialised along with a number of objects.

For example, a camera has a shutter that is usually closed and blinks open to allow in light when you take a
photograph; the shutter is ``c.shutter``, and can be open or closed, cocked or uncocked, and has a timer (how long it
remains open when it's released).

Oher examples are a film advance mechanism, and an exposure mechanism. Many of these subsystems interact with each
other. For example in this camera, advancing the film also cocks the shutter.

Actions that you'd perform with a physical camera are methods of the Python objects. For example, once you have
instantiated a camera, you can advance the film, then trip the shutter::

    >>> c = Camera()
    >>> c.film_advance_mechanism.advance()
    >>> c.shutter.trip()
    Shutter openening for 1/128 seconds
    Shutter closes
    Shutter uncocked
    'Tripped'


Why?
~~~~

I love film cameras and their mechanisms, and spend a lot of time repairing and servicing them. The mechanisms in a
camera are full of functional logic, and thinking about how they change their own state and trigger changes in and
depend on the mechanisms they are connected to is the same kind of thinking that goes on in object-oriented programming.

This project is an experiement in expressing the logic of a camera - in this case, a `Canonet G-III QL17
<https://en.wikipedia.org/wiki/Canonet_G-III_QL17>`_ rangefinder, one of my favourites - in code.
