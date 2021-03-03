import pytest, math

from camera import Camera, Shutter, FilmAdvanceMechanism, LightMeter, ExposureControlSystem, Film


class TestShutter(object):


    def test_trip_when_uncocked(self):
        shutter = Shutter()
        assert shutter.closed == True
        assert shutter.trip() == None
        assert shutter.closed == True

    def test_trip_when_cocked(self):
        shutter = Shutter()
        shutter.cock()
        assert shutter.closed == True
        assert shutter.cocked == True
        assert shutter.trip() == "Tripped"
        assert shutter.closed == True
        assert shutter.cocked == False

    def test_cock_when_cocked(self):
        shutter = Shutter()
        shutter.cock()
        with pytest.raises(Shutter.AlreadyCocked):
            shutter.cock()


class TestFilmAdvanceMechanism(object):

    def test_advance_film(self):
        f = FilmAdvanceMechanism()
        assert f.advanced == False
        f.advance()
        assert f.advanced == True

    def test_advance_film_twice(self):
        f = FilmAdvanceMechanism()
        f.advance()
        with pytest.raises(FilmAdvanceMechanism.AlreadyAdvanced):
            f.advance()

    def test_advance_film_mechanism_with_film(self):
        c = Camera()
        c.film = Film(frames=1)
        c.film_advance_mechanism.advance()
        c.shutter.trip()
        with pytest.raises(Film.NoMoreFrames):
            c.film_advance_mechanism.advance()


class TestFilmAdvanceMechanismShutterInterlock(object):

    def test_film_advance_cocks_shutter(self):
        # advancing film cocks shutter
        c = Camera()
        c.film_advance_mechanism.advance()
        assert c.shutter.cocked == True

        # after the film has been advanced, it can't be advanced again
        with pytest.raises(FilmAdvanceMechanism.AlreadyAdvanced):
            c.film_advance_mechanism.advance()

        # after tripping the shutter, it can be advanced
        assert c.shutter.trip() == "Tripped"
        c.film_advance_mechanism.advance()
        assert c.film_advance_mechanism.advanced == True


class TestLightMeter(object):

    def test_no_battery_no_light(self):
        l = LightMeter()
        assert l.reading() == None

    def test_no_battery(self):
        l = LightMeter(incident_light=0, battery=1.44)
        assert l.reading() == 0

    def test_no_light(self):
        l = LightMeter(incident_light=4096, battery=0)
        assert l.reading() == None

    def test_battery_and_light(self):
        l = LightMeter(incident_light=4096, battery=1.44)
        assert l.reading() == 4096

    def test_lens_cap_on(self):
        c = Camera()
        c.lens_cap.on = True
        assert c.exposure_control_system.light_meter.reading() == 0

    def test_lens_cap_off(self):
        c = Camera()
        c.lens_cap.on = False
        assert c.exposure_control_system.light_meter.reading() == 4096



class TestExposureControlSystem(object):

    def test_measured_ev(self):
        c = Camera()
        assert c.exposure_control_system.measured_ev() == 15.0

    def test_measured_ev_200(self):
        c = Camera()
        c.exposure_control_system.film_speed = 200
        assert c.exposure_control_system.measured_ev() == 16

    def test_measured_ev_more_light(self):
        c = Camera()
        c.environment.scene_luminosity = 8192
        assert c.exposure_control_system.measured_ev() == 16

    def test_measured_ev_less_light(self):
        c = Camera()
        c.environment.scene_luminosity = 1024
        assert c.exposure_control_system.measured_ev() == 13

    def test_measured_ev_0(self):
        c = Camera()
        c.environment.scene_luminosity = 0.125
        assert c.exposure_control_system.measured_ev() == 0

    def test_target_luminance_0(self):
        c = Camera()
        c.environment.scene_luminosity = 0
        assert c.exposure_control_system.measured_ev() == -math.inf

    def test_measured_ev_lens_cap_on(self):
        c = Camera()
        c.lens_cap.on = True
        assert c.exposure_control_system.measured_ev() == -math.inf

    def test_shutter_priority(self):
        c = Camera()
        assert c.shutter.timer == 1/128
        c.exposure_control_system.act()
        assert c.iris.aperture == math.pow(2, c.exposure_control_system.measured_ev()/2) * math.sqrt(1/128)

    def test_shutter_priority_more_light(self):
        c = Camera()
        c.environment.scene_luminosity = 8192
        c.exposure_control_system.act()
        assert c.iris.aperture == math.pow(2, c.exposure_control_system.measured_ev()/2) * math.sqrt(1/128)

    def test_shutter_priority_very_low_light(self):
        c = Camera()
        c.environment.scene_luminosity = 32
        c.exposure_control_system.act()
        assert c.iris.aperture == 1.7


class TestFilm(object):

    def test_no_more_film(self):
        f = Film(frames=1)
        f.advance()
        with pytest.raises(Film.NoMoreFrames):
            f.advance()
