import asyncio
import curses
import random

from tools.sleep import sleep


def get_stars(canvas, num):
  ''' Получить необходимое количество звезд-корутин.
  
  :param canvas: объект холста
  :type canvas: canvss
  :param num: количество звезд
  :type num: int
  '''
  stars = [get_random_star(canvas) for _ in range(num)]
  return stars


def get_random_star(canvas):
    ''' Создать корутину, рисующую звезду.

    :param canvas: объект холста
    :type canvas: canvas
    '''
    offset_tics = random.randint(1, 40)
    y_max, x_max = canvas.getmaxyx()
    column = random.randint(1, x_max - 2)
    row = random.randint(1, y_max - 2)
    star = blink(canvas, offset_tics, column, row)
    return star


async def blink(canvas, offset_tics, column, row):
    ''' Анимация звезды. 
    
    У звезды 4 фазы. Для того, чтобы они мигали асинхронно, первая фаза случайна.
    
    :param canvas: объект холста
    :type canvas: canvas
    :param offset_tics: время действия первой фазы
    :type offset_tics: int
    :param column: координата на холсте
    :type column: int
    :param row: координата на холсте
    :type row: int
    '''
    symbols = ['*', ':', '=', '+', '-']
    symbol = random.choice(symbols)
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(offset_tics)

        canvas.addstr(row, column, symbol)
        await sleep(3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(5)

        canvas.addstr(row, column, symbol)
        await sleep(3)
