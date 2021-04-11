C is for Camera
===============

A 35mm camera, based on the `Canonet G-III QL17 <https://en.wikipedia.org/wiki/Canonet_G-III_QL17>`_ rangefinder,
represented in Python.

The purpose of this project is to explore and understand the logic in the mechanisms of a camera by using
object-oriented programming to represent real-world objects. It's also a way to appreciate the intricate mechanical
logic embodied in a device like a camera.

The level of modelling so far varies - in the exposure control system, the mechanism is modelled down to the level
of individual levers and their interactions. In fact some of the modelling goes down to the level of parts that are not
even detailed separately in Canon's repair manual.

See :ref:`understanding-camera` for more about *how* the camera is modelled.

.. image:: /images/QL17.jpg
   :alt: 'Canonet G-III QL17'


Quick example
--------------

::

    >>> from camera import Camera
    >>> c = Camera()
    >>> c.film_advance_lever.wind()
    On frame 0 (of 24)
    Advancing film
    On frame 1 (of 24)
    Cocking shutter
    Applying aperture value ƒ/1.7 to iris
    Cocked
    >>> c.shutter_button.press()
    Light meter reading: ƒ1/16
    Applying aperture value ƒ/16 to iris
    Shutter opening for 1/128 seconds
    Shutter closes
    Shutter uncocked


See :ref:`get-started` for more.


Contents
--------

..  toctree::
    :maxdepth: 2

    get-started
    how-to
    reference
    explanation

(See `Diátaxis framework <https://diataxis.fr/>`_ for the documentation structure.)
