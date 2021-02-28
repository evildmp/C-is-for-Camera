import pytest

from camera import Camera, Shutter, FilmAdvanceMechanism


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
