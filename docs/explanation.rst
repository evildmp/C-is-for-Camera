.. _explanation:

Explanation
-----------

.. _understanding-camera:

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
