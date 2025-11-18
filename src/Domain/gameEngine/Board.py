""" it is an interface class for creating board
based on its shape and size it is initiated and used by the game engine
"""
from typing import List

from Domain.gameEngine.Cell import Cell

class Board:

        def __init__(self, num_row:int, num_col:int):
            if num_col is None or num_row is None:
                raise TypeError("Board must have num_col and num_row")
            if num_col < 0 or num_row < 0:
                raise IndexError("Board: row and/or column out of range with row=",num_row, ", and column=" , num_col)

            self._num_col = num_col
            self._num_row = num_row
            self._grid: List[List[Cell]] = []

            for i in range(self._num_row):
                row: List[Cell] = []
                for j in range(self._num_col):
                    row.append(Cell())
                self._grid.append(row)

        def get_snapshot(self) -> List[List[str]]:
            """
            Return a snapshot of the board as list[list[str]].
              - ""  if the cell is empty otherwise "player id"
            """
            snapshot: List[List[str]] = []

            for row in range(self._num_row):
                row_snapshot: List[str] = []
                for col in range(self._num_col):
                    cell = self._grid[row][col]

                    if cell.is_empty:
                        row_snapshot.append("")
                    else:
                        row_snapshot.append(str(cell.get_current_user))
                snapshot.append(row_snapshot)

            return snapshot

        def _validate_coordinates(self, row: int, column: int) -> None:
            """Raise IndexError if (row, column) is out of bounds."""
            if not (0 <= row < self._num_row):
                raise IndexError("Board: row out of range")
            if not (0 <= column < self._num_col):
                raise IndexError("Board: column out of range")

        def selectCell(self, row: int, column: int, player_id : str):
            self._validate_coordinates(row, column)
            self._grid[row][column].select_cell(player_id)

        def unSelectCell(self, row: int, column: int):
            self._validate_coordinates(row, column)
            self._grid[row][column].is_selected = False

        def isEmptyCell(self, row: int, column: int)->bool:
            self._validate_coordinates(row, column)
            return self._grid[row][column].is_empty
