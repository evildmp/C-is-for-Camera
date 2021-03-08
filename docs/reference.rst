.. _reference:

Reference
=========

Components of the camera
------------------------

There isn't much you can do with a ``Camera`` object itself. Just as in real life, a camera is really just a
light-tight box; it's all the other components that make up its mechanisms that are interesting. When a ``Camera`` is
instantiated, these other components are also instantiated, as attributes of it.

In addition, things like a roll of film and the physical environment in which the camera finds itself will also be
instantiated, and available as attributes of the camera.

Let's assume that we have created a camera with ``c = Camera()``. In that case, your camera will include a number of
components that allow you to perform various actions, or can be in various states.


Attributes, properties and methods of ``Camera``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``c.state()``: reports the state of the camera and its sub-systems
* ``c.frame_counter``: how many frames the camera indicates have been exposed
* ``c.shutter_speed`` (property): sets ``c.shutter.timer``; for example a nominal 1/30s speed will set the shutter
  timer to 1/32s

So far, other settings and controls need to be accessed through the the sub-systems - for example, to fire the shutter,
you need to do ``c.shutter.trip()``, because a shutter button has not yet been implemented on ``Camera`` itself.


Some things you can do
~~~~~~~~~~~~~~~~~~~~~~

* ``c.film_advance_mechanism.advance()``: advance the film inside the camera and cock the shutter
* ``c.film_rewind_mechanism.rewind()``: wind the film back into the cartridge
* ``c.shutter.trip()``: release the shutter (i.e. actually take a photo)
* ``c.exposure_control_system.meter()``: depending on various things including its own mode, the ambient light, whether
  the lens cap is on, the film speed, the shutter speed, etc, will set the iris aperture
* ``c.exposure_control_system.light_meter.reading()``: takes a reading of the ambient light
* ``c.back.open()`` and ``c.back.close()``: open and close the back - beware of opening the back in daylight with a
  half-exposed roll of film inside


Internal actions
^^^^^^^^^^^^^^^^

There are also some things you can do such as ``c.shutter.cock()``, which you wouldn't or even couldn't do, unless you
had the camera partially disassembled in front of you. In normal use, such actions are only the effect of some other
action (in this case, of advancing the film).


Some states of the objects
~~~~~~~~~~~~~~~~~~~~~~~~~~

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

* ``Camera.NonExistentShutterSpeed``
* ``FilmAdvanceMechanism.AlreadyAdvanced``
* ``Shutter.AlreadyCocked``
* ``Film.NoMoreFrames``

On the other hand, attempting to call ``Shutter.trip()`` when the shutter is not cocked simply does nothing. It doesn't
violate any logic, it just doesn't have any effect.
