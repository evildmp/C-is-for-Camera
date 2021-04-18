import pytest, math

from camera import (
    Camera, ShutterButton, FilmAdvanceLever, Shutter, FilmAdvanceMechanism, LightMeter, ExposureControlSystem,
    ShutterReleaseLever, ExposureLevelLever, ExposureBoundsLever, EELever, Film
    )

class TestCamera(object):

    def test_film_advance_increments_counter(self):
        c = Camera()
        c.film_advance_mechanism.advance()
        c.exposure_control_system.shutter.trip()
        assert c.frame_counter == 1

    def test_selected_shutter_speeds_are_applied(self):
        c = Camera()
        c.shutter_speed = 1/500
        assert c.exposure_control_system.shutter.timer == 1/512
        c.shutter_speed = 1/15
        assert c.exposure_control_system.shutter.timer == 1/16
        c.shutter_speed = 1/125
        assert c.exposure_control_system.shutter.timer == 1/128
        with pytest.raises(c.NonExistentShutterSpeed):
            c.shutter_speed = 1/10

    def test_selected_film_speeds_are_applied(self):
        c = Camera()
        c.film_speed = 400
        assert c.film_speed == 400
        with pytest.raises(c.NonExistentFilmSpeed):
            c.film_speed = 130

    def test_selected_aperture_settings_are_applied_to_exposure_control_system(self):
        c = Camera()
        c.aperture = 8
        assert c.exposure_control_system.aperture_set_lever.aperture == 8

    def test_selected_aperture_settings_are_applied_when_shutter_is_cocked(self):
        c = Camera()
        c.exposure_control_system.shutter.cocked = True
        c.aperture = 8
        assert c.exposure_control_system.iris.aperture == 8
        c.aperture = 2
        assert c.exposure_control_system.iris.aperture == 2
        c.aperture = 16
        assert c.exposure_control_system.iris.aperture == 16

    def test_only_decreasing_aperture_settings_are_applied_when_shutter_is_uncocked(self):
        c = Camera()
        c.exposure_control_system.shutter.cocked = False
        c.aperture = 8
        c.exposure_control_system.iris.aperture = 8
        assert c.exposure_control_system.iris.aperture == 8
        c.aperture = 2
        assert c.exposure_control_system.iris.aperture == 8
        c.aperture = 16
        assert c.exposure_control_system.iris.aperture == 16

    def test_aperture_setting_is_applied_as_soon_as_shutter_is_cocked(self):
        c = Camera()
        c.exposure_control_system.shutter.cocked = False
        c.aperture = 8
        c.exposure_control_system.iris.aperture = 16
        assert c.exposure_control_system.iris.aperture == 16
        c.exposure_control_system.shutter.cock()
        assert c.exposure_control_system.iris.aperture == 8

    def test_invalid_aperture_settings_are_rejected(self):
        c = Camera()
        with pytest.raises(c.ApertureOutOfRange):
            c.aperture = 1.2
        with pytest.raises(c.ApertureOutOfRange):
            c.aperture = 22


class TestShutterButton(object):

    def test_button_not_in_camera_cannot_be_pressed(self):
        sb = ShutterButton()
        with pytest.raises(ShutterButton.CannotBePressed):
            sb.press()

    def test_button_trips_shutter(self):
        c = Camera()
        c.film_advance_lever.wind()
        c.shutter_button.press()
        assert c.exposure_control_system.shutter.cocked == False
        assert c.film_advance_mechanism.advanced == False


class TestFilmAdvanceLever(object):

    def test_lever_not_on_camera_cannot_be_pressed(self):
        l = FilmAdvanceLever()
        with pytest.raises(FilmAdvanceLever.CannotBeWound):
            l.wind()

    def test_lever_advances_mechanism(self):
        c = Camera()
        assert c.exposure_control_system.shutter.cocked == False
        assert c.film_advance_mechanism.advanced == False
        c.film_advance_lever.wind()
        assert c.exposure_control_system.shutter.cocked == True
        assert c.film_advance_mechanism.advanced == True


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
        c.exposure_control_system.shutter.trip()
        with pytest.raises(Film.NoMoreFrames):
            c.film_advance_mechanism.advance()


class TestFilmRewindMechanism(object):

    def test_rewind_film_mechanism_with_film(self):
        c = Camera()
        c.film.frame = 10
        c.film_rewind_mechanism.rewind()
        assert c.film.frame == 0
        assert c.film.fully_rewound == True


class TestFilmAdvanceMechanismShutterInterlock(object):

    def test_film_advance_cocks_shutter(self):
        # advancing film cocks shutter
        c = Camera()
        c.film_advance_mechanism.advance()
        assert c.exposure_control_system.shutter.cocked == True

        # after the film has been advanced, it can't be advanced again
        with pytest.raises(FilmAdvanceMechanism.AlreadyAdvanced):
            c.film_advance_mechanism.advance()

        # after tripping the shutter, it can be advanced
        assert c.exposure_control_system.shutter.trip() == "Tripped"
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

    def test_theoretical_aperture(self):
        c = Camera()
        c.environment.scene_luminosity = 16
        assert pytest.approx(c.exposure_control_system.theoretical_aperture()) == 1
        c.environment.scene_luminosity = 1024
        assert pytest.approx(c.exposure_control_system.theoretical_aperture()) == 8
        c.environment.scene_luminosity = 4096
        assert pytest.approx(c.exposure_control_system.theoretical_aperture()) == 16
        c.environment.scene_luminosity = 16384
        assert pytest.approx(c.exposure_control_system.theoretical_aperture()) == 32

    def test_shutter_priority_less_light(self):
        c = Camera()
        c.environment.scene_luminosity = 1456
        c.exposure_control_system.meter()
        assert c.exposure_control_system.meter() == c.exposure_control_system.theoretical_aperture()
        c.environment.scene_luminosity = 3565
        assert c.exposure_control_system.meter() == c.exposure_control_system.theoretical_aperture()

    def test_shutter_priority_not_enough_light(self):
        c = Camera()
        c.environment.scene_luminosity = 32
        assert c.exposure_control_system.meter() == "Under"

    def test_shutter_priority_too_much_light(self):
        c = Camera()
        c.environment.scene_luminosity = 16384
        assert c.exposure_control_system.meter() == "Over"

    def test_manual_mode(self):
        c = Camera()
        c.exposure_control_system.mode = "Manual"
        assert c.exposure_control_system.meter() is None
        assert c.exposure_control_system.iris.aperture == 16

    def test_exposure_meter(self):
        c = Camera()
        for sl in range(0, 17000, 1000):
            assert  c.exposure_indicator() == c.exposure_control_system.read_meter()

    def test_new_film_speed_setting_is_applied_to_ecs(self):
        c = Camera()
        assert c.exposure_control_system.film_speed == 100
        c.film_speed = 400
        assert c.exposure_control_system.film_speed == 400


class TestShutterReleaseLever(object):

    def test_nothing_happens_when_there_is_no_exposure_control_system(self):
        srl = ShutterReleaseLever()
        assert srl.depress() == None

    def test_depress_lever_in_manual_mode_is_not_blocked(self):
        ecs = ExposureControlSystem()
        ecs.mode = "Manual"
        ecs.shutter.cock()
        ecs.shutter_release_lever.depress()
        assert ecs.shutter.cocked == False

    def test_depress_lever_in_AE_mode_is_blocked(self):
        ecs = ExposureControlSystem()
        assert ecs.mode == "Shutter priority"
        assert ecs.meter() == None
        ecs.shutter.cock()
        ecs.shutter_release_lever.depress()
        assert ecs.shutter.cocked == True

    def test_depress_lever_in_bright_light(self):
        c = Camera()
        ecs = c.exposure_control_system
        assert ecs.meter() == 16
        assert ecs.mode == "Shutter priority"
        ecs.shutter.cock()
        ecs.shutter_release_lever.depress()
        assert ecs.shutter.cocked == False

    def test_depress_lever_in_too_bright_light(self):
        c = Camera()
        c.environment.scene_luminosity = 8096
        ecs = c.exposure_control_system
        assert ecs.meter() == "Over"
        assert ecs.mode == "Shutter priority"
        ecs.shutter.cock()
        ecs.shutter_release_lever.depress()
        assert ecs.shutter.cocked == True

    def test_depress_lever_in_dim_light(self):
        c = Camera()
        c.environment.scene_luminosity = 256
        ecs = c.exposure_control_system
        assert pytest.approx(ecs.meter()) == 4
        assert ecs.mode == "Shutter priority"
        ecs.shutter.cock()
        ecs.shutter_release_lever.depress()
        assert ecs.shutter.cocked == False

    def test_depress_lever_in_too_dim_light(self):
        c = Camera()
        c.environment.scene_luminosity = 32
        ecs = c.exposure_control_system
        assert ecs.meter() == "Under"
        assert ecs.mode == "Shutter priority"
        ecs.shutter.cock()
        ecs.shutter_release_lever.depress()
        assert ecs.shutter.cocked == True


class TestExposureLevelLever(object):

    def test_nothing_happens_when_there_is_no_exposure_control_system(self):
        ell = ExposureLevelLever()
        assert ell.activate() is None

    def test_can_be_activated_in_manual_mode_because_it_is_not_blocked(self):
        ecs = ExposureControlSystem()
        ecs.mode = "Manual"
        assert ecs.exposure_level_lever.activate() == "Activated EE lever"

    def test_cannot_be_activated_in_AE_mode_because_it_is_blocked(self):
        ecs = ExposureControlSystem()
        assert ecs.mode == "Shutter priority"
        assert ecs.meter() == None
        assert ecs.exposure_level_lever.activate() == "Blocked"


class TestExposureBoundsLever(object):

    def test_nothing_happens_when_there_is_no_exposure_control_system(self):
        ebl = ExposureBoundsLever()
        assert ebl.activate() is None

    def test_cannot_be_activated_in_manual_mode_because_it_is_blocked(self):
        ecs = ExposureControlSystem()
        ecs.mode = "Manual"
        assert ecs.exposure_bounds_lever.activate() == "Blocked"

    def test_can_be_activated_in_AE_mode_because_it_is_not_blocked(self):
        ecs = ExposureControlSystem()
        assert ecs.mode == "Shutter priority"
        assert ecs.meter() == None
        assert ecs.exposure_bounds_lever.activate() == "Activated shutter lock lever"


class TestEELever(object):

    def test_nothing_happens_when_there_is_no_exposure_control_system(self):
        eel = EELever()
        assert eel.locked() == None

    def test_locked_in_manual_mode_and_not_locked_in_AE_mode(self):
        ecs = ExposureControlSystem(mode="Manual")
        assert ecs.ee_lever.locked() == True
        ecs.mode = "Shutter priority"
        assert ecs.ee_lever.locked() == False

    def test_eelever_(self):
        c = Camera()
        ecs = c.exposure_control_system
        assert ecs.mode == "Shutter priority"
        assert pytest.approx(ecs.ee_lever.activate(16)) == 16


class TestShutterLockLever(object):

    def test_nothing_happens_when_there_is_no_exposure_control_system(self):
        ecs = ExposureControlSystem()
        assert ecs.shutter_lock_lever.activate() == None
        assert ecs.shutter_lock_lever.deactivate() == None


    def test_activation_locks(self):
        ecs = ExposureControlSystem()
        ecs.shutter_lock_lever.activate()
        assert ecs.shutter_lock_lever.blocks == True
        ecs.shutter_lock_lever.deactivate()
        assert ecs.shutter_lock_lever.blocks == False


class TestApertureSetLever(object):

    def test_lever_is_only_set_by_camera_in_manual_mode(self):
        c = Camera()
        c.aperture = "A"
        assert c.exposure_control_system.aperture_set_lever.aperture == 16

    def test_when_shutter_is_cocked_all_aperture_ring_movement_controls_iris(self):
        ecs = ExposureControlSystem()
        ecs.mode = "Manual"
        ecs.shutter.cock()
        ecs.aperture_set_lever.aperture = 8
        assert ecs.aperture_set_lever.aperture == 8
        assert ecs.iris.aperture == 8
        ecs.aperture_set_lever.aperture = 16
        assert ecs.aperture_set_lever.aperture == 16
        assert ecs.iris.aperture == 16
        ecs.aperture_set_lever.aperture = 2
        assert ecs.aperture_set_lever.aperture == 2
        assert ecs.iris.aperture == 2

    def test_when_shutter_is_uncocked_all_iris_only_closes_further_in_response_to_aperture_ring_movement(self):
        ecs = ExposureControlSystem()
        ecs.mode = "Manual"
        ecs.aperture_set_lever._aperture = 8
        # decreasing aperture setting closes iris, moves lever
        ecs.aperture_set_lever.aperture = 16
        assert ecs.aperture_set_lever.aperture == 16
        assert ecs.iris.aperture == 16
        # increasing aperture setting has no effect on iris
        ecs.aperture_set_lever.aperture = 2
        assert ecs.aperture_set_lever.aperture == 2
        assert ecs.iris.aperture == 16

    def test_when_cocking_the_shutter_the_iris_immediately_responds(self):
        ecs = ExposureControlSystem()
        ecs.mode = "Manual"
        ecs.aperture_set_lever.aperture = 16
        assert ecs.aperture_set_lever.aperture == 16
        assert ecs.iris.aperture == 16
        # change the setting but nothing happens
        ecs.aperture_set_lever.aperture = 2
        assert ecs.aperture_set_lever.aperture == 2
        assert ecs.iris.aperture == 16
        # until the shutter is cocked
        ecs.shutter.cock()
        assert ecs.iris.aperture == 2

    def test_when_shutter_is_cocked_depressing_release_controls_iris(self):
        c = Camera()
        c.exposure_control_system.shutter.cock()
        c.environment.scene_luminosity = 1024
        c.exposure_control_system.mode = "Shutter priority"
        assert pytest.approx(c.exposure_control_system.meter()) == 8
        c.shutter_button.press()
        assert pytest.approx(c.exposure_control_system.aperture_set_lever.aperture) == 8
        assert pytest.approx(c.exposure_control_system.iris.aperture) == 8

    def test_when_shutter_is_uncocked_depressing_release_can_only_close_iris(self):
        c = Camera()
        c.environment.scene_luminosity = 1024
        c.exposure_control_system.iris.aperture = 8
        c.exposure_control_system.mode = "Shutter priority"
        assert pytest.approx(c.exposure_control_system.meter()) == 8
        c.shutter_button.press()
        assert pytest.approx(c.exposure_control_system.aperture_set_lever.aperture) == 8
        assert pytest.approx(c.exposure_control_system.iris.aperture) == 8

        c.environment.scene_luminosity = 256
        assert pytest.approx(c.exposure_control_system.meter()) == 4
        c.shutter_button.press()
        assert pytest.approx(c.exposure_control_system.aperture_set_lever.aperture) == 4
        assert pytest.approx(c.exposure_control_system.iris.aperture) == 8

        c.environment.scene_luminosity = 4096
        assert pytest.approx(c.exposure_control_system.meter()) == 16
        c.shutter_button.press()
        assert pytest.approx(c.exposure_control_system.aperture_set_lever.aperture) == 16
        assert pytest.approx(c.exposure_control_system.iris.aperture) == 16

    def test_when_cocking_the_shutter_the_iris_opens_as_wide_as_possible(self):
        ecs = ExposureControlSystem()
        ecs.mode = "Shutter priority"
        assert ecs.aperture_set_lever.aperture == 16
        assert ecs.iris.aperture == 16
        ecs.shutter.cock()
        assert ecs.aperture_set_lever.aperture == 1.7
        assert ecs.iris.aperture == 1.7


    #
    # * aperture-priority mode, when:
    #
    #   * shutter is cocked, depressing the shutter release lever adjusts the iris to the auto-exposure aperture (if in range)
    #   * shutter is uncocked, depressing the shutter release lever only adjusts the iris to a smaller auto-exposure aperture
    #     (if in range)
    #   * cocking the shutter, the iris is immediately adjusted to the widest possible aperture


class TestFilm(object):

    def test_no_more_film(self):
        f = Film(frames=1)
        f.advance()
        with pytest.raises(Film.NoMoreFrames):
            f.advance()


class TestBack(object):

    def test_opening_resets_frame_counter_and_does_not_harm_film(self):
        c = Camera()
        c.frame_counter = 5
        c.back.open()
        assert c.frame_counter == 0
        assert c.back.open() != "Film is ruined"
        assert c.film.ruined == False

    def test_opening_back_in_daylight_ruins_film(self):
        c = Camera()
        c.film.frame = 5
        assert c.back.open() == "Film is ruined"
        assert c.film.ruined == True

    def test_opening_back_in_dark_is_ok(self):
        c = Camera()
        c.environment.scene_luminosity = 0
        c.film.frame = 5
        assert c.back.open() != "Film is ruined"
        assert c.film.ruined == False

    def test_opening_with_rewound_film_is_ok(self):
        c = Camera()
        c.film.frame = 5
        c.film_rewind_mechanism.rewind()
        assert c.back.open() != "Film is ruined"
        assert c.film.ruined == False


class TestRegressions(object):

    def test_we_can_do_state_after_winding(self):
        c = Camera()
        c.film_advance_lever.wind()
        c.state()

    def test_we_can_do_state_when_over_or_under(self):
        c = Camera()
        c.state()
        c.film_speed = 400
        c.aperture = "A"
        c.shutter_speed = 1/125
        c.state()
