from curses_tools import draw_frame
import asyncio

async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


async def fill_orbit_with_garbage(canvas, coroutines_roster):
  garbage_roster = ['garb_duck', 
                            'garb_hubble',
                            'garb_lamp',
                            'garb_trash_large',
                            'garb_trash_small',
                            'garb_trash_x1']
  while True:
    x = random.randint(0, 50)
    with open('garbage_obj/' + random.choice(garbage_roster)+ '.txt', "r") as garb_file:
      frame = garb_file.read()
    coroutines_roster.append(fly_garbage(canvas, x, frame))
    await asyncio.sleep(0)
