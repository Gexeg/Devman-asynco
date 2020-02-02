import asyncio

from tools.curses_tools import draw_frame
from tools.sleep import sleep


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


def get_garbage_delay_tics(year):
    if year < 1961:
        return None
    elif year < 1969:
        return 20
    elif year < 1981:
        return 14
    elif year < 1995:
        return 10
    elif year < 2010:
        return 8
    elif year < 2020:
        return 6
    else:
        return 2
 

class Scenario():
    def __init__(self):
        self.counter = 0
        self.year = 1957
        self.spaceship_has_cannon = False
        self.clean_space = True

    def tick(self):
        self.counter += 1
        if self.counter == 15:
            self.year += 1
            self.counter = 0


    def get_year(self):
        return self.year

    def turn_cannon(self):
        return self.year > 2019

    def turn_garbage(self):
        if self.year > 1961:
            if self.clean_space:
                self.clean_space = False
                return True
            return False



scenario = Scenario()
