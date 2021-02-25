import time, math

class Camera:
    def __init__(self):
        self.shutter = Shutter()
        self.iris = Iris()
        self.back = Back()
        self.exposure_control_system = ExposureControlSystem(mode="Shutter priority", camera=self, battery=1.44)
        self.film_advance_mechanism = FilmAdvanceMechanism(camera=self)
        self.lens_cap = LensCap(on=False)
        self.environment = Environment()

    def state(self):
        print("================== Camera state =================")
        print()
        print("------------------ Mechanical -------------------")
        print(f"Back closed:               {self.back.closed}")
        print(f"Lens cap on:               {self.lens_cap.on}")
        print(f"Film advance mechanism:    {self.film_advance_mechanism.advanced}")
        print(f"Shutter cocked:            {self.shutter.cocked}")
        print(f"Shutter timer:             1/{1/self.shutter.timer} seconds")
        print(f"Iris aperture:             ƒ/{self.iris.aperture}")
        print(f"Camera exposure settings:  {math.log(math.pow(self.iris.aperture, 2)/self.shutter.timer, 2)} EV")
        print()

        print("------------------ Metering ---------------------")
        print(f"Light meter reading:        {self.exposure_control_system.light_meter.reading()} cd/m^2")
        print(f"Exposure target:            {self.exposure_control_system.target_ev()} EV")
        print(f"Mode:                       {self.exposure_control_system.mode}")
        print(f"Battery:                    {self.exposure_control_system.battery} V")
        print(f"Film speed:                 {self.exposure_control_system.film_speed} ISO")
        print()

        print("------------------ Environment ------------------")
        print(f"Scene luminosity:           {self.environment.scene_luminosity} cd/m^2")



class FilmAdvanceMechanism:
    def __init__(self, camera=None):
        self.camera = camera
        self.advanced = False

    def advance(self):
        if self.camera and self.camera.shutter:
            try:
                self.advanced = True
                self.camera.shutter.cock()
            except self.camera.shutter.AlreadyCocked:
                pass

class Shutter:
    # The shutter is closed by default.
    def __init__(self, timer=1/128, closed=True, cocked=False):
        self.timer = timer
        self.closed = closed
        self.cocked = cocked

    def trip(self):
        # The shutter may only be tripped if it's already cocked - otherwise,
        # nothing at all happens.
        if not self.closed or not self.cocked:
            return
        print("Shutter opens")
        time.sleep(self.timer)
        self.closed = True
        print("Shutter closes")
        print("Shutter opened for 1/{} seconds".format(int(1/self.timer)))
        self.cocked = False
        print("Shutter uncocked")

    def cock(self):
        if self.cocked:
            raise self.AlreadyCocked

        else:
            print("Cocking shutter")
            self.cocked = True
            print("Cocked")

    class AlreadyCocked(Exception):
        pass

class Iris:

    def __init__(self, aperture=16):
        self.aperture = aperture

class ExposureControlSystem:

    #     math.log(
    #             (reading * self.film_speed/12.5),2
    #         )

    def __init__(self, mode="Manual", film_speed=100, camera=None, battery=None):
        self.mode = mode
        self.film_speed = film_speed
        self.camera = camera
        self.battery = battery

        self.light_meter = LightMeter(camera=self.camera, battery=self.battery)

    def target_ev(self):
        if self.light_meter.reading():
            return math.log(
                (self.light_meter.reading() * self.film_speed/12.5),2
            )
        else:
            return -math.inf

    def act(self):
        if self.mode == "Manual":
            pass
        elif self.mode == "Shutter priority":
            timer = self.camera.shutter.timer
            target_aperture = math.pow(2, self.target_ev()/2) * math.sqrt(timer)
            if target_aperture < 1.7:
                aperture = 1.7
            else:
                aperture = target_aperture
            self.camera.iris.aperture = aperture

class LightMeter:

    def __init__(self, camera=None, incident_light = 0, battery=None):
        self.camera = camera
        self.incident_light = incident_light
        self.battery = battery

    def reading(self):
        if self.battery:

            # If the light meter has not been removed from the camera, we will take the
            # measurement from the camera's environment - if the lens cap is not on.
            if self.camera:
                if self.camera.lens_cap.on:
                    return 0
                else:
                    return self.camera.environment.scene_luminosity

            # If the rest of the camera is not around, we can still measure incident light on the
            # meter.
            else:
                return self.incident_light


class Back:
    # The back is closed by default.
    def __init__(self, closed=True):
        self.closed = closed

    def close(self):
        if not self.closed:
            self.closed = True
            print("Closing back")
        print("Back is closed")

    def open(self):
        if self.closed:
            self.closed = False
            print("Opening back")
        print("Back is open")

class LensCap:
    # The lens cap is on by default.
    def __init__(self, on=True):
        self.on = on

class Environment:
    def __init__(self, scene_luminosity = 4096):
        self.scene_luminosity = scene_luminosity