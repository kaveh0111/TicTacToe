""" it is an interface class for creating board
based on its shape and size it is initiated and used by the game engine
"""
from typing import List

from .Cell import Cell

class Board:

    def __init__(self, num_col:int, num_row:int):
        self._num_col = num_col
        self._num_row = num_row
        self._grid: List[List[Cell]] = []

        for i in range(self._num_col):
            row: List[Cell] = []
            for j in range(self._num_row):
                row.append(Cell(__col=i, __row=j))
            self._grid.append(row)


        def selectCell(column: int, row: int):
            if (0 >= column) and (column > self._num_col):
                raise IndexError("Board: column out of range for selected cell")
            if (0 >= row) and (row > self._num_row):
                raise IndexError("Board: row out of range for selected cell")
            self._grid[column][row].is_selected = True

        def unSelectCell(column: int, row: int):
            if (0 >= column) and (column > self._num_col):
                raise IndexError("Board: column out of range for Unselected cell")
            if (0 >= row) and (row > self._num_row):
                raise IndexError("Board: row out of range for  Unselected cell")
            self._grid[column][row].is_selected = False

