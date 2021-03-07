c is for Camera
===============

A 35mm camera, based on the `Canonet G-III QL17 <https://en.wikipedia.org/wiki/Canonet_G-III_QL17>`_ rangefinder,
represented in Python.

The purpose of this project is to explore and understand the logic in the mechanisms of a camera by using
object-oriented programming to represent real-world objects. It's also a way to appreciate the intricate mechanical
logic embodied in a device like a camera.

See :ref:`understanding-camera` for more about *how* the camera is simulated.

.. image:: /images/QL17.jpg
   :alt: 'Canonet G-III QL17'

::

    >>> from camera import Camera
    >>> c = Camera()
    >>> c.film_advance_mechanism.advance()
    On frame 0 (of 24)
    Advancing film
    On frame 1 (of 24)
    Cocking shutter
    Cocked
    >>> c.shutter.trip()
    Shutter openening for 1/128 seconds
    Shutter closes
    Shutter uncocked
    'Tripped'

See :ref:`get-started` for more.


Contents
--------

..  toctree::
    :maxdepth: 2

    get-started
    how-to
    reference
    explanation
