from tkinter import Button, Label
import random
import settings
import ctypes
import sys

class Cell:
    # Attributes
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label = None
    mine_count = settings.MINE_COUNT
    mine_count_label = None

    # Constructor
    def __init__(self, x, y, is_mine = False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_flagged = False
        self.is_zero = False
        self.cell_btn = None
        self.x = x
        self.y = y

        # Append the object to the Cell.all list
        Cell.all.append(self)

    # Button Constructor
    def create_btn_object(self, location):
        btn = Button(
            location,
            width = 2,                                     # change size
            height = 1,
        )
        btn.bind('<Button-1>', self.left_click_events) # Left Click
        btn.bind('<Button-3>', self.right_click_events) # Right Click
        self.cell_btn = btn
    
    # Displays info about the number of cells
    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg = 'black',                                   # change color
            fg = 'white',
            text = f"Cells Left: {Cell.cell_count}",
            font = ("", 15)
        )
        Cell.cell_count_label = lbl

        # Displays info about the number of mines
    @staticmethod
    def create_mine_count_label(location):
        lbl = Label(
            location,
            bg = 'black',                                   # change color
            fg = 'white',
            text = f"Mines Left: {Cell.mine_count}",
            font = ("", 15)
        )
        Cell.mine_count_label = lbl

    # Left Click Events
    def left_click_events(self, event):
        if not self.is_flagged:
            if self.is_mine:
                self.game_over()
            else:
                self.show_cell()
                self.show_zero_mines()

                # checks if the player won
                if Cell.cell_count == settings.MINE_COUNT:
                    ctypes.windll.user32.MessageBoxW(0, 'You win!', 'Game Over', 0)             # check other message boxes
                    sys.exit()
            
            # cancels Left and Right Click events
            self.cell_btn.unbind('<Button-1>')
            self.cell_btn.unbind('<Button-3>')

    # Return a cell object based on the value of x, y
    def get_cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    # Checks which are the surrounding cells
    @property # to use it as an attribute
    def surrounding_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x, self.y + 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
        ]
        
        # Eliminating non-existing cells from the array
        cells = [cell for cell in cells if cell is not None]
        return cells

    # Counts the surrounding mines
    @property
    def surrounding_mines(self):
        counter = 0
        for cell in self.surrounding_cells:
            if cell.is_mine:
                counter += 1

        return counter

    # Reveals the cells surrounding 0
    def show_zero_mines(self):
        if self.surrounding_mines == 0:
            self.is_zero = True
            for cell_obj in self.surrounding_cells:
                cell_obj.show_cell()
                cell_obj.cell_btn.unbind('<Button-3>')
                if cell_obj.surrounding_mines == 0 and cell_obj.is_zero == False:
                    cell_obj.show_zero_mines()
        return 1

    # Reveals the cell number
    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn.configure(text = self.surrounding_mines)
            # updates Cell Count label
            if Cell.cell_count_label:
                Cell.cell_count_label.configure(text = f"Cells Left: {Cell.cell_count}")
            
        # marks cell as opened (Use as last line)
        self.is_opened = True 

    # Interrupts the game and display "Game Over" message
    def game_over(self):
        ctypes.windll.user32.MessageBoxW(0, 'You clicked on a mine...', 'Game Over', 0)     # check other message boxes
        sys.exit()
    
    # Right Click Event
    def right_click_events(self, event):
        if not self.is_flagged:
            self.cell_btn.configure(bg = 'orange')
            Cell.mine_count -= 1
            # updates Mine Count label
            if Cell.mine_count_label:
                Cell.mine_count_label.configure(text = f"Mines Left: {Cell.mine_count}")
            self.is_flagged = True
        else:
            self.cell_btn.configure(bg = 'SystemButtonFace')
            Cell.mine_count += 1
            # updates Mine Count label
            if Cell.mine_count_label:
                Cell.mine_count_label.configure(text = f"Mines Left: {Cell.mine_count}")
            self.is_flagged = False

    # Assigning mines randomly to the cells
    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all, settings.MINE_COUNT
        )
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    # Renaming the console name of the cells to a clean format
    def __repr__(self):
        return f"Cell({self.x}, {self.y})"