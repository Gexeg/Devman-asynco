import asyncio
from tools.curses_tools import draw_frame, get_frame_size

game_оver = '''
   _____                         ____                 
  / ____|                       / __ \                
 | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ 
 | | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|
 | |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |   
  \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|   
'''


async def show_gameover(canvas):
   ''' Отрисовать game over в центре экрана.
   
   :param canvas: [description]
   :type canvas: [type]
   '''
   y_max, x_max = canvas.getmaxyx()
   length, width = get_frame_size(game_оver)
   row = y_max // 2 - length
   column = x_max // 2 - width

   while True:
      draw_frame(canvas, row, column, game_оver)
      await asyncio.sleep(0)