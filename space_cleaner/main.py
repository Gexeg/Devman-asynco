import asyncio
import curses
import random
import time

from space_objects.stars import blink
from space_objects.rocket import rocket_animation


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
    coroutines.append(rocket_animation.draw_space_ship(canvas))
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


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
