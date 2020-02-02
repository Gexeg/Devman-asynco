import asyncio
import curses
import random
import time

from space_objects.stars import blink
from space_objects.rocket.rocket_animation import animate_spaceship, run_spaceship
from space_objects.garbage.fly_garbage import fly_garbage, obstacles, obstacles_last_collision
from tools.obstacles import show_obstacles
from tools.explosion import explode
from tools.game_scenario import PHRASES, get_garbage_delay_tics, scenario
from tools.curses_tools import draw_frame
from tools.sleep import sleep


async def fill_orbit_with_garbage(canvas, coroutines: list):
    ''' Генерирует новые корутины с падающим мусором.
    
    :param canvas: экземлпяр холста
    :type canvas: canvas
    :param coroutines: список корутин
    :type coroutines: list
    :param tics: интервал между появлением нового мусора
    :type tics: int
    :yield: корутину - падающий мусор
    :rtype: coroutine
    '''
    global scenario

    while True:
        _, x_max = canvas.getmaxyx()
        column = random.randint(1, x_max - 2)
        coroutines.append(fly_garbage(canvas, column))
        tics = get_garbage_delay_tics(scenario.get_year())
        await sleep(tics)


async def draw_year(canvas):
    ''' Отрисовать текущий год и достижение (если было). 
    
    :param canvas: [description]
    :type canvas: [type]
    '''
    global scenario
    y_max, x_max = canvas.getmaxyx()
    row = y_max - 2
    column = x_max // 2
    while True:
        if scenario.get_year() in PHRASES:
            phrase = ': {}'.format(PHRASES[scenario.get_year()])
        else:
            phrase = ''
        year_frame = '{}{}'.format(scenario.get_year(), phrase)
        draw_frame(canvas, row, column, year_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, year_frame, negative=True)


def draw_star(canvas):
    ''' Нарисовать звезду.

    :param canvas: объект холста
    :type canvas: canvas
    '''
    offset_tics = random.randint(1, 40)
    y_max, x_max = canvas.getmaxyx()
    column = random.randint(1, x_max - 2)
    row = random.randint(1, y_max - 2)
    star = blink(canvas, offset_tics, column, row)
    return star


def get_event_loop(canvas):
    ''' Создать основной список корутин.

    :param canvas: объект холста
    :type canvas: canvas
    '''
    coroutines = []
    coroutines.append(draw_year(canvas))
    coroutines.append(animate_spaceship())
    coroutines.append(run_spaceship(canvas, coroutines))
    for _ in range(50):
        coroutines.append(draw_star(canvas))
    return coroutines


def canvas_setup(canvas):
    ''' Первичные настройки холста

    :param canvas: объект холста
    :type canvas: canvas
    '''
    canvas.border()
    curses.curs_set(False)
    canvas.nodelay(True)


def main(canvas):
    ''' Основной цикл, запускающий корутины с анимациями. '''
    global scenario

    canvas_setup(canvas)
    coroutines = get_event_loop(canvas)
    while True:
        for coroutine in coroutines:
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(0.1)
        scenario.tick()
        if scenario.turn_garbage():
            coroutines.append(fill_orbit_with_garbage(canvas, coroutines))


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
