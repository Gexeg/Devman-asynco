import asyncio
import curses
import random


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
