import time, math

class Camera:

    selectable_shutter_speeds = {
        1/4:1/4, 1/8:1/8, 1/15:1/16, 1/30:1/32, 1/60:1/64, 1/125:1/128, 1/250:1/256, 1/500:1/512
    }
    selectable_film_speeds = (25, 50, 100, 200, 400, 800)

    def __init__(self):
        # set up sub-systems
        self.shutter = Shutter(camera=self)
        self.iris = Iris(camera=self)
        self.back = Back(camera=self)
        self.exposure_control_system = ExposureControlSystem(
            mode="Shutter priority", camera=self, film_speed=100, battery=1.44
        )
        self.film_advance_mechanism = FilmAdvanceMechanism(camera=self)
        self.film_rewind_mechanism = FilmRewindMechanism(camera=self)
        self.lens_cap = LensCap(on=False)
        self.film = Film(camera=self)
        self.environment = Environment()

        # set up camera settings and indicators
        self.frame_counter = 0
        self.film_speed = 100
        self.shutter_speed = 1/125
        self.exposure_indicator = self.exposure_control_system.meter

        self.shutter_button = ShutterButton(camera=self)
        self.film_advance_lever = FilmAdvanceLever(camera=self)
        self.aperture = "A"


    # ----------- Camera settings -----------

    @property
    def shutter_speed(self):
        return self._shutter_speed

    @shutter_speed.setter
    def shutter_speed(self, value):
        if not value in self.selectable_shutter_speeds:
            possible_settings = ", ".join([f"1/{int(1/s)}" for s in self.selectable_shutter_speeds.keys()])
            raise self.NonExistentShutterSpeed(f"Possible shutter speeds are {possible_settings}")

        self.shutter.timer = self.selectable_shutter_speeds[value]
        self._shutter_speed = value

    class NonExistentShutterSpeed(Exception):
        pass


    @property
    def aperture(self):
        return self._aperture

    @aperture.setter
    def aperture(self, value):
        if value == "A":
            self.exposure_control_system.mode = "Shutter priority"
            self.exposure_control_system.meter()

        elif not 1.7 <= value <= 16:
            raise self.ApertureOutOfRange

        else:
            self.iris.set_aperture(value)

        self._aperture = value


    class ApertureOutOfRange(Exception):
        pass


    @property
    def film_speed(self):
        return self._film_speed

    @film_speed.setter
    def film_speed(self, value):
        if not value in self.selectable_film_speeds:
            possible_settings = ", ".join([f"{s}" for s in self.selectable_film_speeds])
            raise self.NonExistentFilmSpeed(f"Possible film speeds are {possible_settings}")

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
        print("------------------ indicators -------------------")
        print(f"Exposure_indicator:        ƒ/{self.exposure_indicator()}")
        print(f"Frame counter:             {self.frame_counter}")
        print()

        print("------------------ Mechanical -------------------")
        print(f"Back closed:               {self.back.closed}")
        print(f"Lens cap on:               {self.lens_cap.on}")
        print(f"Film advance mechanism:    {self.film_advance_mechanism.advanced}")
        print(f"Shutter cocked:            {self.shutter.cocked}")
        print(f"Shutter timer:             1/{int(1/self.shutter.timer)} seconds")
        print(f"Iris aperture:             ƒ/{self.iris.aperture}")
        print(f"Camera exposure settings:  {math.log(math.pow(self.iris.aperture, 2)/self.shutter.timer, 2)} EV")
        print()

        print("------------------ Metering ---------------------")
        print(f"Light meter reading:        {self.exposure_control_system.light_meter.reading()} cd/m^2")
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

        self.camera.shutter.trip()

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

            if self.camera.shutter:
                self.camera.shutter.cock()

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


class Shutter:
    # The shutter is closed by default.
    def __init__(self, camera=None, timer=1/128, closed=True, cocked=False):
        self.camera = camera
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

        if self.camera:
            self.camera.film_advance_mechanism.advanced = False

        return "Tripped"

    def cock(self):
        if self.cocked:
            raise self.AlreadyCocked

        print("Cocking shutter")
        self.cocked = True

        # cocking the shutter causes the aperture value to be applied to the iris
        if self.camera:
            print("Applying aperture value to iris")
            self.camera.iris.set_aperture(self.camera.aperture)

        print("Cocked")
        return "Cocked"

    class AlreadyCocked(Exception):
        pass


class Iris:

    def __init__(self, camera=None, aperture=16):
        self.camera = camera
        self.aperture = aperture

    def set_aperture(self, value):

        # when the shutter is cocked, the iris follows the aperture setting
        if self.camera.shutter.cocked:
            self.aperture = value

        # when the shutter is uncocked, the iris only closes in response to aperture setting changes
        elif value > self.aperture:
            self.aperture = value



class ExposureControlSystem:

    def __init__(self, mode="Manual", film_speed=100, camera=None, battery=None):
        self.mode = mode
        self.film_speed = film_speed
        self.camera = camera
        self.battery = battery

        self.light_meter = LightMeter(camera=self.camera, battery=self.battery)

    def measured_ev(self):
        if not self.light_meter.reading():
            return -math.inf

        return math.log((self.light_meter.reading() * self.film_speed/12.5),2)

    def theoretical_aperture(self):
        return math.pow(2, self.measured_ev()/2) * math.sqrt(self.camera.shutter.timer)

    def meter(self):
        if self.mode == "Manual":
            return

        if self.theoretical_aperture() < 1.7:
            aperture = 1.7
        elif self.theoretical_aperture() > 16:
            aperture = 16
        else:
            aperture = self.theoretical_aperture()
        self.camera.iris.aperture = aperture

        return aperture


class LightMeter:

    def __init__(self, camera=None, incident_light=0, battery=None):
        self.camera = camera
        self.incident_light = incident_light
        self.battery = battery

    def reading(self):
        if not self.battery:
            return

        # If the light meter has not been removed from the camera, we will take the
        # measurement from the camera's environment - if the lens cap is not on.
        if not self.camera:
            # If the rest of the camera is not around, we can still measure incident light on the meter.
            return self.incident_light

        if self.camera.lens_cap.on:
            return 0

        return self.camera.environment.scene_luminosity


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


