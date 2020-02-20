class SpaceGlobals():
    def __init__(self):
        self.year_frame = ''
        self.clean_space = True
        self.plasma_gun = False
        self.garbage_delay_tics = None


class Scenario():

    PHRASES = {
        # Только на английском, Repl.it ломается на кириллице
        1957: "First Sputnik",
        1961: "Gagarin flew!",
        1969: "Armstrong got on the moon!",
        1971: "First orbital space station Salute-1",
        1981: "Flight of the Shuttle Columbia",
        1998: 'ISS start building',
        2011: 'Messenger launch to Mercury',
        2020: "Take the plasma gun! Shoot the garbage!",
    }

    def __init__(self, space_globals):
        self.space_globals = space_globals
        self.counter = 0
        self.year = 1957
        self.set_year_frame()

    def tick(self):
        self.counter += 1
        if self.counter == 15:
            self.year += 1
            self.counter = 0
            if self.year == 1962:
                self.space_globals.clean_space = False
            if self.year == 2020:
                self.space_globals.plasma_gun = True
            self.space_globals.garbage_delay_tics = self._get_garbage_delay_tics()
            self.set_year_frame()

    def set_year_frame(self):
        if self.year in self.PHRASES:
            phrase = self.PHRASES[self.year]
            year_frame = '{}: {}'.format(self.year, phrase)
        else:
            year_frame = str(self.year)
        self.space_globals.year_frame = year_frame

    def _get_garbage_delay_tics(self):
        if self.year < 1961:
            return None
        elif self.year < 1969:
            return 20
        elif self.year < 1981:
            return 14
        elif self.year < 1995:
            return 10
        elif self.year < 2010:
            return 8
        elif self.year < 2020:
            return 6
        else:
            return 2

space_globals = SpaceGlobals()
scenario = Scenario(space_globals)
