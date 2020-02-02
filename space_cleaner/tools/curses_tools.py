def draw_frame(canvas, start_row, start_column, text, negative=False):
    '''Draw multiline text fragment on canvas. Erase text instead of drawing if negative=True is specified.'''
    
    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break
                
            if symbol == ' ':
                continue

            # Check that current position it is not in a lower right corner of the window
            # Curses will raise exception in that case. Don`t ask why…
            # https://docs.python.org/3/library/curses.html#curses.window.addch
            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


def get_frame_with_info(filepath: str) -> tuple((str, int, int)):
    ''' Прочитать кадр из файла.

    :param filepath: путь к фрейму
    :type filepath: str
    '''
    with open(filepath, 'r') as file:
        frame = file.read()
        rows = frame.split('\n')
        length = len(rows)
        width = max([len(row) for row in rows])
        return frame, length, width


def get_frame_size(frame: str):
    ''' Определить размеры переданного кадра.
    
    :param frame: кадр
    :type frame: str
    '''
    rows = frame.split('\n')
    length = len(rows)
    width = max([len(row) for row in rows])
    return length, width
