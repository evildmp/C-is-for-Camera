import pytest

from camera import Camera, Shutter, FilmAdvanceMechanism


class TestShutter(object):

    shutter = Shutter()

    def test_trip_when_uncocked(self):
        assert self.shutter.closed == True
        assert self.shutter.trip() == None
        assert self.shutter.closed == True

    def test_trip_when_cocked(self):
        self.shutter.cocked = False
        self.shutter.cock()
        assert self.shutter.closed == True
        assert self.shutter.cocked == True
        assert self.shutter.trip() == "Tripped"
        assert self.shutter.closed == True

    def test_cock_when_cocked(self):
        self.shutter.cock()
        with pytest.raises(Shutter.AlreadyCocked):
            self.shutter.cock()


class TestFilmAdvanceMechanism(object):

    f = FilmAdvanceMechanism()

    def test_advance_film(self):
        assert self.f.advanced == False
        self.f.advance()
        assert self.f.advanced == True

    def test_advance_film_twice(self):
        self.f.advanced = True
        with pytest.raises(FilmAdvanceMechanism.AlreadyAdvanced):
            self.f.advance()


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
