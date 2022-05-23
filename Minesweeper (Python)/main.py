from tkinter import *
from cell import Cell
import settings
import utils

root = Tk()

# Override the settings of the window
root.configure(bg = "blue")                            # Change background color
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
root.title("Minesweeper Game")
root.resizable(False, False)

# ----Header Frame----
top_frame = Frame(
    root,
    bg = 'black',                                       # Change color
    width = settings.WIDTH,
    height = settings.HEADER_MARGIN
)
top_frame.place(x = 0, y = 0)

# Title
game_title = Label(
    top_frame,
    bg = 'black',
    fg = 'white',
    text = 'Minesweeper',
    font = ('', 24)
)
game_title.place(x = utils.width_prct(40), y = 0)

# ----Info Frame----
left_frame = Frame(
    root,
    bg = 'black',                                       # Change color
    width = settings.INDEX_MARGIN,
    height = settings.GRID_SIZE * 26
)
left_frame.place(x = 0, y = settings.HEADER_MARGIN)

# Call the labels from the Cell class
Cell.create_cell_count_label(left_frame)
Cell.cell_count_label.place(x = 0, y = 0)

Cell.create_mine_count_label(left_frame)
Cell.mine_count_label.place(x = 0, y = 40)

# ----Game Frame----
center_frame = Frame(
    root,
    bg = 'blue',                                       # Change color
    width = settings.GRID_SIZE * 24,
    height = utils.height_prct(75)
)
center_frame.place(
    x = settings.INDEX_MARGIN,
    y = settings.HEADER_MARGIN
)

# Cells Generator
for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c = Cell(x, y)
        c.create_btn_object(center_frame)
        c.cell_btn.grid(column = x, row = y)

Cell.randomize_mines()

# Run the window
root.mainloop()