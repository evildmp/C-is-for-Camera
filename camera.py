import time, math

class Camera:

    selectable_shutter_speeds = {
        1/4:1/4, 1/8:1/8, 1/15:1/16, 1/30:1/32, 1/60:1/64, 1/125:1/128, 1/250:1/256, 1/500:1/512
    }
    selectable_film_speeds = (25, 50, 100, 200, 400, 800)

    def __init__(self):
        # set up sub-systems
        self.back = Back(camera=self)
        self.exposure_control_system = ExposureControlSystem(
            mode="Shutter priority", camera=self, film_speed=100, battery=1.44
        )
        self.film_advance_mechanism = FilmAdvanceMechanism(camera=self)
        self.film_rewind_mechanism = FilmRewindMechanism(camera=self)
        self.lens_cap = LensCap(on=False)
        self.film = Film(camera=self)
        self.environment = Environment(scene_luminosity=4096)

        # set up camera settings and indicators
        self.frame_counter = 0
        self.film_speed = 100
        self.shutter_speed = 1/125
        self.aperture = "A"
        self.exposure_indicator = self.exposure_control_system.read_meter

        self.shutter_button = ShutterButton(camera=self)
        self.film_advance_lever = FilmAdvanceLever(camera=self)


    # ----------- Camera settings -----------

    # The camera will only allow the shutter speeds marked on the shutter ring to be applied, and will
    # raise an exception if you try to set shutter_speed to an illegal value.
    @property
    def shutter_speed(self):
        return self._shutter_speed

    @shutter_speed.setter
    def shutter_speed(self, value):
        if not value in self.selectable_shutter_speeds:
            possible_settings = ", ".join([f"1/{int(1/s)}" for s in self.selectable_shutter_speeds.keys()])
            raise self.NonExistentShutterSpeed(f"Possible shutter speeds are {possible_settings}")

        self.exposure_control_system.shutter.timer = self.selectable_shutter_speeds[value]
        self._shutter_speed = value

    class NonExistentShutterSpeed(Exception):
        pass


    # The camera will only allow the aperture settings marked on the aperture ring to be applied, and will
    # raise an exception if you try to set aperture to an illegal value.
    @property
    def aperture(self):
        return self._aperture

    @aperture.setter
    def aperture(self, value):
        if value == "A":
            self.exposure_control_system.mode = "Shutter priority"

        elif not 1.7 <= value <= 16:
            raise self.ApertureOutOfRange

        else:
            self.exposure_control_system.mode = "Manual"
            self.exposure_control_system.aperture_set_lever.aperture = value

        self._aperture = value


    class ApertureOutOfRange(Exception):
        pass


    # The camera will only allow the film speed settings marked on the aperture ring to be applied, and will
    # raise an exception if you try to set the film speed to an illegal value.
    @property
    def film_speed(self):
        return self._film_speed

    @film_speed.setter
    def film_speed(self, value):
        if not value in self.selectable_film_speeds:
            possible_settings = ", ".join([f"{s}" for s in self.selectable_film_speeds])
            raise self.NonExistentFilmSpeed(f"Possible film speeds are {possible_settings}")

        self.exposure_control_system.film_speed = value
        self._film_speed = value

    class NonExistentFilmSpeed(Exception):
        pass


    # ----------- Reporting -----------

    def state(self):
        print("================== Camera state =================")
        print()
        print("------------------ Controls ---------------------")
        print(f"Film speed:                {self.film_speed} ISO")
        print(f"Selected speed:            1/{int(1/self.shutter_speed)}")
        print()
        print("------------------ Indicators -------------------")
        print(f"Exposure indicator         {self.exposure_indicator()}")
        print(f"Frame counter:             {self.frame_counter}")
        print()

        print("------------------ Mechanical -------------------")
        print(f"Back closed:               {self.back.closed}")
        print(f"Lens cap on:               {self.lens_cap.on}")
        print(f"Film advance mechanism:    {self.film_advance_mechanism.advanced}")
        print(f"Shutter cocked:            {self.exposure_control_system.shutter.cocked}")
        print(f"Shutter timer:             1/{int(1/self.exposure_control_system.shutter.timer)} seconds")
        print(f"Iris aperture:             ƒ/{self.exposure_control_system.iris.aperture:.2g}")
        print(f"Camera exposure settings:  {self.exposure_control_system.exposure_value()} EV")
        print()

        print("------------------ Metering ---------------------")
        print(f"Metered light:              {self.exposure_control_system.light_meter.reading()} cd/m^2")
        print(f"Exposure target:            {self.exposure_control_system.measured_ev()} EV")
        print(f"Mode:                       {self.exposure_control_system.mode}")
        print(f"Battery:                    {self.exposure_control_system.battery} V")
        print(f"Film speed:                 {self.exposure_control_system.film_speed} ISO")
        print()

        print("------------------ Film -------------------------")
        print(f"Speed:                      {self.film.speed} ISO")
        print(f"Rewound into cartridge:     {self.film.fully_rewound}")
        print(f"Exposed frames:             {self.film.frame} (of {self.film.frames})")
        print(f"Ruined:                     {self.film.ruined}")
        print()

        print("------------------ Environment ------------------")
        print(f"Scene luminosity:           {self.environment.scene_luminosity} cd/m^2")

# ----------- Controls -----------

class ShutterButton(object):

    def __init__(self, camera=None):
        self.camera = camera

    def press(self):
        if not self.camera:
            raise self.CannotBePressed

        self.camera.exposure_control_system.shutter_release_lever.depress()

    class CannotBePressed(Exception):
        pass


class FilmAdvanceLever(object):

    def __init__(self, camera=None):
        self.camera = camera

    def wind(self):
        if not self.camera:
            raise self.CannotBeWound

        self.camera.film_advance_mechanism.advance()

    class CannotBeWound(Exception):
        pass


# ----------- Subsystems -----------

class FilmAdvanceMechanism:
    def __init__(self, camera=None):
        self.camera = camera
        self.advanced = False

    def advance(self):
        if self.advanced:
            raise self.AlreadyAdvanced

        self.advanced = True

        if self.camera:

            if self.camera.film:
                self.camera.film.advance()

            if self.camera.exposure_control_system.shutter:
                self.camera.exposure_control_system.shutter.cock()

    class AlreadyAdvanced(Exception):
        pass


class FilmRewindMechanism:
    def __init__(self, camera=None):
        self.camera = camera

    def rewind(self):
        if not self.camera.film:
            return

        self.camera.film.frame = 0
        self.camera.film.fully_rewound = True
        print("Rewinding film")


class ExposureControlSystem:

    def __init__(self, mode="Shutter priority", film_speed=100, camera=None, battery=None):
        self.mode = mode
        self.film_speed = film_speed
        self.camera = camera
        self.battery = battery

        self.light_meter = LightMeter(exposure_control_system=self, battery=self.battery)
        self.shutter = Shutter(exposure_control_system=self)
        self.iris = Iris(exposure_control_system=self)

        self.shutter_release_lever = ShutterReleaseLever(exposure_control_system=self)
        self.shutter_lock_lever = ShutterLockLever(exposure_control_system=self)
        self.ee_lever = EELever(exposure_control_system=self)
        self.exposure_level_lever = ExposureLevelLever(exposure_control_system=self)
        self.exposure_bounds_lever = ExposureBoundsLever(exposure_control_system=self)
        self.aperture_set_lever = ApertureSetLever(exposure_control_system=self)

    # measured_ev is the exposure value from the system (that the aperture will need to
    # respond to) and is determined by the light reading and the film-speed.
    def measured_ev(self):
        if self.light_meter.reading() is None:
            return None
        elif self.light_meter.reading() == 0:
            return -math.inf

        return math.log((self.light_meter.reading() * self.film_speed/12.5),2)

    # the aperture that the system needs to set in order to match the measure_ev
    def theoretical_aperture(self):
        if self.measured_ev() is None:
            return

        return math.pow(2, self.measured_ev()/2) * math.sqrt(self.shutter.timer)

    def meter(self):
        if self.mode == "Manual" or self.theoretical_aperture() is None:
            return

        theoretical_aperture = self.theoretical_aperture()

        if theoretical_aperture < 1.7 and math.isclose(theoretical_aperture, 1.7):
            reading = 1.7
        elif theoretical_aperture > 16 and math.isclose(theoretical_aperture, 16):
           reading = 16
        elif theoretical_aperture < 1.7:
            reading = "Under"
        elif theoretical_aperture > 16:
            reading = "Over"
        else:
            reading = theoretical_aperture
        return reading

    # what the meter needle actually shows (but only if the camera is actually metering)
    def read_meter(self):
        if self.meter():
            if type(self.meter()) is not str:
                return f"ƒ/{self.meter():.2g}"
            else:
                return self.meter()


    def exposure_value(self):
        # returns the EV of the exposure system
        if self.mode == "Manual":
            return math.log(math.pow(self.iris.aperture, 2)/self.shutter.timer, 2)
        else:
            return "Shutter priority"

class Shutter:
    def __init__(self, exposure_control_system=None, timer=1/128, closed=True, cocked=False):
        self.exposure_control_system = exposure_control_system
        self.timer = timer
        self.closed = closed
        self.cocked = cocked

    def trip(self):
        # The shutter may only be tripped if it's already cocked - otherwise,
        # nothing at all happens.
        if not self.closed or not self.cocked:
            return

        print(f"Shutter opening for 1/{int(1/self.timer)} seconds")
        time.sleep(self.timer)
        self.closed = True
        print("Shutter closes")
        self.cocked = False
        print("Shutter uncocked")

        if self.exposure_control_system and self.exposure_control_system.camera:
            self.exposure_control_system.camera.film_advance_mechanism.advanced = False

        return "Tripped"

    def cock(self):
        if self.cocked:
            raise self.AlreadyCocked

        print("Cocking shutter")
        self.cocked = True

        # cocking the shutter causes the set_aperture_lever value to be applied to the iris
        if self.exposure_control_system:
            if self.exposure_control_system.mode == "Shutter priority":
                self.exposure_control_system.aperture_set_lever.aperture = 1.7
            self.exposure_control_system.iris.aperture = self.exposure_control_system.aperture_set_lever.aperture
            print(f"Applying aperture value ƒ/{self.exposure_control_system.aperture_set_lever.aperture:.2g} to iris")

        print("Cocked")
        return "Cocked"

    class AlreadyCocked(Exception):
        pass


class ShutterReleaseLever:
    # part number 19-0562

    def __init__(self, exposure_control_system=None):
        self.exposure_control_system = exposure_control_system

    def depress(self):

        if not self.exposure_control_system:
            return

        self.exposure_control_system.exposure_level_lever.activate()
        self.exposure_control_system.read_meter()

        if self.exposure_control_system.shutter_lock_lever.blocks:
            self.exposure_control_system.exposure_level_lever.deactivate()
            print("Shutter release blocked")
            return

        if self.exposure_control_system.mode == "Shutter priority":
            aperture = self.exposure_control_system.aperture_set_lever.aperture
            if self.exposure_control_system.shutter.cocked:
                self.exposure_control_system.iris.aperture = aperture
            elif aperture > self.exposure_control_system.iris.aperture:
                self.exposure_control_system.iris.aperture = aperture

            print(f"Applying aperture value ƒ/{self.exposure_control_system.aperture_set_lever.aperture:.2g} to iris")

        self.exposure_control_system.shutter.trip()

        self.exposure_control_system.exposure_level_lever.deactivate()


class ExposureLevelLever:
    # no individual part number available

    def __init__(self, exposure_control_system=None):
        self.exposure_control_system = exposure_control_system

    def activate(self):
        if not self.exposure_control_system:
            return

        self.exposure_control_system.exposure_bounds_lever.activate()

        if not self.exposure_control_system.shutter_lock_lever.blocks:
            meter_value = self.exposure_control_system.meter()
            self.exposure_control_system.ee_lever.activate(meter_value)
            return "Activated EE lever"

        else:
            return "Blocked"

    def deactivate(self):
        if not self.exposure_control_system:
            return

        self.exposure_control_system.ee_lever.deactivate()


class ExposureBoundsLever:
    # no individual part number available

    def __init__(self, exposure_control_system=None):
        self.exposure_control_system = exposure_control_system

    def activate(self):
        if not self.exposure_control_system:
            return
        elif self.exposure_control_system.ee_lever.locked():
            return "Blocked"

        meter_value = self.exposure_control_system.meter()

        if meter_value is None or meter_value == "Under" or meter_value == "Over":
            self.exposure_control_system.shutter_lock_lever.activate()
            return "Activated shutter lock lever"

    def deactivate(self):
        if not self.exposure_control_system:
            return

        self.exposure_control_system.shutter_lock_lever.activate()


class ShutterLockLever:
    # part number 19-0566

    def __init__(self, exposure_control_system=None):
        self.exposure_control_system = exposure_control_system
        self.blocks = False

    def activate(self):
        if not self.exposure_control_system:
            return

        self.blocks = True

    def deactivate(self):
        if not self.exposure_control_system:
            return

        self.blocks = False


class EELever:

    def __init__(self, exposure_control_system=None):
        self.exposure_control_system = exposure_control_system

        if exposure_control_system:
            self.position = 0  # 0 is rotated fully anti-clockwise; 1 is rotated fully clockwise

    def activate(self, aperture_value):
        if self.locked():
            return "Locked"

        self.exposure_control_system.aperture_set_lever.aperture = aperture_value

        return aperture_value

    def deactivate(self):
        if not self.exposure_control_system:
            return

    def locked(self):
        if not self.exposure_control_system:
            return
        return self.exposure_control_system.mode == "Manual"


class ApertureSetLever:
    # part number Y13-5255 (I think)
    # the lever is partially decoupled from the iris; only under certain circumstances does the iris
    # respond to it

    def __init__(self, exposure_control_system=None, aperture=16):
        self.exposure_control_system = exposure_control_system
        self._aperture = aperture
        # self.aperture = aperture

    @property
    def aperture(self):
        return self._aperture

    @aperture.setter
    def aperture(self, value):
        # when the shutter is cocked, the aperture_set_lever follows the aperture setting
        if self.exposure_control_system.mode == "Manual":
            if self.exposure_control_system.shutter.cocked:
                self.exposure_control_system.iris.aperture = value
            elif value > self.aperture:
                self.exposure_control_system.iris.aperture = value
        self._aperture = value


class Iris:

    def __init__(self, exposure_control_system=None, aperture=16):
        self.exposure_control_system = exposure_control_system
        self.aperture = aperture


class LightMeter:

    def __init__(self, exposure_control_system=None, incident_light=0, battery=None):
        self.exposure_control_system = exposure_control_system
        self.incident_light = incident_light
        self.battery = battery

    def reading(self):
        if not self.battery:
            return

        # If the light meter has not been removed from the camera, we will take the
        # measurement from the camera's environment - if the lens cap is not on.
        if not self.exposure_control_system:
            # If the rest of the camera is not around, we can still measure incident light on the meter.
            return self.incident_light

        if self.exposure_control_system.camera.lens_cap.on:
            return 0

        return self.exposure_control_system.camera.environment.scene_luminosity


class Back:
    # The back is closed by default.
    def __init__(self, camera, closed=True):
        self.closed = closed
        self.camera = camera

    def close(self):
        if not self.closed:
            self.closed = True
            print("Closing back")

    def open(self):
        if not self.closed:
            return

        self.closed = False
        print("Opening back")
        self.camera.frame_counter = 0

        if self.camera.film.frame == 0:
            return

        print("Resetting frame counter to 0")
        if self.camera.environment.scene_luminosity > 0 and self.camera.film:
            self.camera.film.ruined = True
            return "Film is ruined"


# ----------- Other objects -----------

class LensCap:
    def __init__(self, on=True):
        self.on = on


class Film:
    def __init__(self, speed=100, frames=24, camera=None, fully_rewound=False):
        self.speed = speed
        self.frames = frames
        self.frame = 0
        self.camera = camera
        self.fully_rewound = fully_rewound
        self.ruined = False

    def advance(self):
        if not self.frame < self.frames:
            raise self.NoMoreFrames

        if self.fully_rewound:
            return

        print(f"On frame {self.frame} (of {self.frames})")
        print("Advancing film")

        self.frame += 1
        if self.camera and self.camera.back.closed == True:
            self.camera.frame_counter += 1
        print(f"On frame {self.frame} (of {self.frames})")

    class NoMoreFrames(Exception):
        pass


class Environment:
    def __init__(self, scene_luminosity=4096):
        self.scene_luminosity = scene_luminosity
