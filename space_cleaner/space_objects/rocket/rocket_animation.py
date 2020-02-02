import asyncio
import curses

from tools.curses_tools import draw_frame, get_frame_with_info
from tools.physics import update_speed
from space_objects.garbage.fly_garbage import obstacles, obstacles_last_collision
from tools.game_over import show_gameover
from tools.explosion import explode
from tools.game_scenario import scenario


spaceship_frame = None


async def animate_spaceship():
    global spaceship_frame
    frame1, _, _ = get_frame_with_info('space_objects/rocket/frames/frame_1.txt')
    frame2, _, _ = get_frame_with_info('space_objects/rocket/frames/frame_2.txt')
    while True:
        spaceship_frame = frame1
        await asyncio.sleep(0)
        spaceship_frame = frame2
        await asyncio.sleep(0)


SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258


def read_controls(canvas):
    '''Read keys pressed and returns tuple witl controls state.'''
    
    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            # https://docs.python.org/3/library/curses.html#curses.window.getch
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -1

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 1

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 1

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -1

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True
    
    return rows_direction, columns_direction, space_pressed


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    '''Display animation of gun shot. Direction and speed can be specified.'''

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        for obstacle in obstacles:
            if obstacle.has_collision(row, column):
                obstacles_last_collision.append(obstacle)
                return
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def run_spaceship(canvas, coroutines):  
    ''' Анимация корабля.'''
    global spaceship_frame
    _, len1, width1 = get_frame_with_info('space_objects/rocket/frames/frame_1.txt')
    _, len2, width2 = get_frame_with_info('space_objects/rocket/frames/frame_2.txt')
    frame_length = max([len1, len2])
    frame_width = max([width1, width2])

    y_max, x_max = canvas.getmaxyx()
    row = y_max // 2
    column = x_max // 2

    row_speed = 0
    column_speed = 0
    
    while True:  
        draw_frame(canvas, row, column, spaceship_frame)
        current_frame = spaceship_frame
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, current_frame, negative=True)

        row_dir, column_dir, space_pressed = read_controls(canvas)
        if space_pressed and scenario.turn_cannon():
            coroutines.append(fire(canvas, row, column + 2))
        row_speed, column_speed = update_speed(row_speed, column_speed, row_dir, column_dir)

        row = row + row_speed
        if row + row_dir + frame_length > y_max:
            row = y_max - frame_length
        elif row + row_dir < 1:
            row = 1

        column = column + column_speed 
        if column + row_dir  + frame_width > x_max - 2:
            column = x_max - frame_width - 2
        elif column + column_dir < 1:
            column = 1

        for obstacle in obstacles:
            if obstacle.has_collision(row, column):
                draw_frame(canvas, row, column, current_frame, negative=True)
                await explode(canvas, row, column)
                coroutines.append(show_gameover(canvas))
                return
