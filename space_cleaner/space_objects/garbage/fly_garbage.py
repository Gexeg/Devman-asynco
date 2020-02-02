import asyncio
import random

from tools.curses_tools import draw_frame, get_frame_with_info
from tools.obstacles import Obstacle
from tools.sleep import sleep
from tools.explosion import explode
from tools.game_scenario import get_garbage_delay_tics


obstacles = []
obstacles_last_collision = []


async def fly_garbage(canvas, column, speed=0.5):
    '''Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start.'''
    global obstacles
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0
    frame, length, width = get_frame_with_info(get_random_garbage_frame())
    obstacle_marker = Obstacle(row, column, length, width)
    obstacles.append(obstacle_marker)
    while row < rows_number:
        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, negative=True)
        row += speed
        obstacle_marker.row = row
        if obstacle_marker in obstacles_last_collision:
            obstacles.remove(obstacle_marker)
            draw_frame(canvas, row, column, frame, negative=True)
            await explode(canvas, obstacle_marker.row, obstacle_marker.column)
            return


def get_random_garbage_frame():
    ''' Получает случайный фрейм для мусора. '''
    garbage_roster = [
      'garb_duck', 
      'garb_hubble',
      'garb_lamp',
      'garb_trash_large',
      'garb_trash_small',
      'garb_trash_x1'
    ]
    path = 'space_objects/garbage/frames/' + random.choice(garbage_roster)+ '.txt'
    return path



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

    while True:
        _, x_max = canvas.getmaxyx()
        column = random.randint(1, x_max - 2)
        coroutines.append(fly_garbage(canvas, column))
        tics = 20
        await sleep(tics)
