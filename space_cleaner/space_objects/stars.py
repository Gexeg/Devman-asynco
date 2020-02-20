import asyncio
import curses
import random


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


async def blink(canvas, offset_tics, column, row):
    ''' анимация звезды. У звезды 4 фазы. Для того, чтобы они мигали асинхронно, первая фаза случайна'''
    symbols = ['*', ':', '=', '+', '-']
    symbol = random.choice(symbols)
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        i = 0
        for i in range(offset_tics):
          i +=1
          await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        i = 0
        for i in range(3):
          i +=1
          await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        i = 0
        for i in range(5):
          i +=1
          await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        i = 0
        for i in range(3):
          i += 1
          await asyncio.sleep(0)
