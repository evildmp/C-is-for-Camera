.. _explanation:

Explanation
===========

.. _understanding-camera:

Understanding ``Camera``
------------------------

A camera is an instance of the ``Camera`` class. When a ``Camera`` is instantiated (``c = Camera()``), it's
initialised along with a number of objects.

For example, a camera has a shutter that is usually closed and blinks open to allow in light when you take a
photograph; the shutter is ``c.shutter``, and can be open or closed, cocked or uncocked, and has a timer (how long it
remains open when it's released).

Other examples are a film advance mechanism, and an exposure mechanism. Many of these subsystems interact with each
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


.. _explanation-numbers:

Representing a physical device in software
-------------------------------------------

Why does the ``Shutter`` default to a shutter speed of 1/128s, which is not a speed you'll see indicated on any camera?

A film camera from the 1970s doesn't have the same precision or accuracy as floating-point operations in software. In
addition, cameras in any case use many nominal numbers in their controls, that only represent an approximation to some
numerical ideal.

The traditional scale of shutter timings for example - 1s, 1/2s, 1/4s, 1/8s, 1/15s, 1/30s, 1/60s, 1/125s, 1/250s -
proceeds roughly in sequential powers of 2, but breaks down twice in just a few steps, in order to provide easier
numbers to work with.

If a shutter had a precise 1s speed and it followed the rule of 2 precisely, then it would have a 1/128s speed -
which it does in software, even if no camera does in real life.

However, the real-life QL17 has shutter speed selector ring that that ``Camera`` also represents. When you apply
a shutter speed::

   c.shutter_speed = 1/125

two things happen. First, it checks whether the selected speed is one of those that the camera actually has, and raises
a :ref:`Camera.NonExistentShutterSpeed <exceptions>` exception if not. If it's a legitimate selection, it applies an
*actual* shutter speed to the shutter (see the next section).


How changing a camera setting changes other settings
----------------------------------------------------

As noted, when you apply value to ``c.shutter_speed``, it also applies it to ``c.shutter.timer``.

It does this with a ``shutter_speed()`` method of ``Camera``, decorated to function as the *setter* for the attribute.

..  code-block:: python

    @shutter_speed.setter
    def shutter_speed(self, value):
        if not value in self.selectable_shutter_speeds:
            possible_settings = ", ".join([f"1/{int(1/s)}" for s in self.selectable_shutter_speeds.keys()])
            raise self.NonExistentShutterSpeed(f"Possible shutter speeds are {possible_settings}")

        self.shutter.timer = self.selectable_shutter_speeds[value]
        self._shutter_speed = value

Similarly, you can set ``c.aperture`` - but the setting will only be accepted if it's one that's actually available,
and if not, you'll get an ``ApertureOutOfRange`` exception.

Only valid values will then be applied to the subsystems.


Why build a 40-year-old camera in Python?
-----------------------------------------

I love film cameras and their mechanisms, and spend a lot of time repairing and servicing them. The mechanisms in a
camera are full of functional logic, and thinking about how they change their own state and trigger changes in and
depend on the mechanisms they are connected to is the same kind of thinking that goes on in object-oriented programming.

This project is an experiment in expressing the logic of a camera - in this case, a `Canonet G-III QL17
<https://en.wikipedia.org/wiki/Canonet_G-III_QL17>`_ rangefinder, one of my favourites - in code.
