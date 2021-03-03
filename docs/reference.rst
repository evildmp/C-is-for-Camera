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
