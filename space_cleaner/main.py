import curses
import time

from space_objects.stars import get_stars
from space_objects.rocket.rocket_animation import animate_spaceship, run_spaceship
from space_objects.garbage.fly_garbage import fill_orbit_with_garbage
from tools.game_scenario import scenario
from tools.game_messages import draw_year


def main(canvas):
    ''' Основной цикл, запускающий корутины с анимациями. '''
    global scenario

    canvas.border()
    curses.curs_set(False)
    canvas.nodelay(True)
    coroutines = [
        draw_year(canvas),
        animate_spaceship(),
        *get_stars(canvas, 50)
    ]
    # Для следующих корутин необходима ссылка на уже объявленную переменную
    coroutines.append(run_spaceship(canvas, coroutines))
    coroutines.append(fill_orbit_with_garbage(canvas, coroutines))
    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        scenario.tick()
        time.sleep(0.1)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
