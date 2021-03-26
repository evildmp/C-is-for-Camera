.. _reference:

Reference
=========

``Camera`` basics
------------------------

There isn't much you can do with a ``Camera`` object itself. Just as in real life, a camera is really just a
light-tight box; it's all the other components that make up its mechanisms that are interesting. When a ``Camera`` is
instantiated, these other components are also instantiated, as attributes of it.

In addition, things like a roll of film and the physical environment in which the camera finds itself will also be
instantiated, and available as attributes of the camera.

Let's assume that we have created a camera with ``c = Camera()``. In that case, your camera will include a number of
components that allow you to perform various actions, or can be in various states, for example::

    >>> from camera import Camera
    >>> c = Camera()
    >>> c.aperture = "A"

All the examples below are similarly attributes of a ``Camera`` instance.


Things you can set on a ``Camera`` instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``aperture`` - "A", or a value between 1.7 and 16 (ƒ-number).
* ``film_speed`` - 25-800 (ISO)
* ``shutter_speed`` - 1/4, 1/8, 1/15, 1/30, 1/60, 1/125, 1/250, 1/500 (seconds; :ref:`nominal values
  <explanation-numbers>`)


Things you do with a ``Camera`` instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``state()``: get a report of the state of the camera and its sub-systems
*  ``film_advance_lever.advance()``
* ``shutter_button.press()``
* ``back.open()`` and ``back.close()`` - beware of opening the back in daylight with a half-exposed roll of film inside


Values you can read from a ``Camera`` instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``frame_counter``: how many frames the camera indicates have been exposed
* ``exposure_indicator()``


Sub-systems
-----------

The sub-systems can be accessed **directly**. For example, you can do things like::

    >>> from camera import Camera
    >>> c = Camera()
    >>> c.shutter.cock()
    Cocking shutter
    Applying aperture value to iris
    Cocked

which you wouldn't or even couldn't do, unless you had the camera partially disassembled in front of you. In normal
use, such actions are only the effect of some other action (in this case, of advancing the film).

You can also make use of sub-systems completely **independently** of a camera object::

    >>> from camera import Shutter
    >>> s = Shutter()
    >>> s.cock()
    Cocking shutter
    Cocked

As in a real camera, sub-systems are affected by each other, which is why in the first example above, cocking the
shutter also applies the aperture value to the iris.


Some notable sub-sytem actions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assuming ``c = Camera()``:

* ``c.film_advance_mechanism.advance()``: advance the film inside the camera and cock the shutter
* ``c.film_rewind_mechanism.rewind()``: wind the film back into the cartridge
* ``c.shutter.trip()``: release the shutter (i.e. actually take a photo)
* ``c.exposure_control_system.meter()``: depending on various things including its own mode, the ambient light, whether
  the lens cap is on, the film speed, the shutter speed, etc, will set the iris aperture
* ``c.exposure_control_system.light_meter.reading()``: takes a reading of the ambient light


Some states of the sub-system objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some of these states are ones that it makes sense for you to set (e.g. how bright it is or whether the lens cap is on)
while others only make sense as reports from the system (such as whether the film has been ruined by something you did).
Some are of both kinds.

* ``c.film_advance_mechanism.advanced``: ``True`` or ``False``
* ``c.shutter.timer``: shutter speed
* ``c.shutter.cocked``: ``True`` or ``False``
* ``c.iris.aperture``
* ``c.lens_cap.on``: ``True`` or ``False``
* ``c.film.frame``: which frame we're on
* ``c.film.frames``: how many frames in the roll
* ``c.film.fully_rewound``: ``True`` or ``False``
* ``c.film.ruined``: ``True`` or ``False``
* ``c.environment.scene_luminosity``: how bright it is


.. _exceptions:

Exceptions
----------

Exceptions occur when you try to do something that the camera refuses to do because it violates the logic of a
mechanism of the camera. For example, if the shutter is already cocked, you can't cock it again; it's not logically
possible to cock a shutter that's already cocked. Some things are logically possible, but not physically possible,
like selecting a shutter speed that this particular camera doesn't have.

Exceptions should be fairly self-explanatory:

* ``Camera``

  * ``NonExistentShutterSpeed``
  * ``ApertureOutOfRange``
  * ``NonExistentFilmSpeed``

* ``FilmAdvanceMechanism.AlreadyAdvanced``
* ``Shutter.AlreadyCocked``
* ``Film.NoMoreFrames``
* ``ShutterButton.CannotBePressed``
* ``FilmAdvanceLever.CannotBeWound``

On the other hand, attempting to call ``Shutter.trip()`` when the shutter is not cocked simply does nothing. It doesn't
violate any logic, it just doesn't have any effect.
