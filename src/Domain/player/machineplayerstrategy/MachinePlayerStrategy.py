import random
from typing import List, Tuple

from Domain.gameEngine.Board import Board
#from Domain.gameEngine.Cell import Cell
from abc import ABC, abstractmethod

from Domain.gameEngine.Cell import Cell


class MachinePlayerStrategy(ABC):

    @abstractmethod
    def play(self, board: Board)->Tuple[int, int]:
        #it returns the optimal next move,
        raise NotImplementedError

class RandomPlayerStrategy(MachinePlayerStrategy):
    def __init__(self, num_rows : int = 3, num_col : int = 3) -> None:
        self._num_rows = num_rows
        self._num_col = num_col

    def play(self, board: Board)->Tuple[int, int]:
        #find a random empty cell and return its row and col number
        empty_cells = self.__getUnselectedCells(board)
        random_cell = random.choice(empty_cells)
        return (random_cell.row, random_cell.col)

    def __getUnselectedCells(self, board: Board)->List[Cell]:
        return_list = []
        for row in range(self._num_rows):
            for col in range(self._num_col):
                if board._grid[row][col] == False:
                    return_list.append(Cell(row, col))



class MinimaxPlayerStrategy(MachinePlayerStrategy):
    def __init__(self, num_rows : int = 3, nom_cols : int = 3) -> None:
        self._num_rows = num_rows
        self._num_col = nom_cols
        if (self._num_rows != 3) or (self._num_col != 3):
            raise ValueError("This policy is only for 3*3 boards")

    def play(self, board: Board)->Tuple[int, int]:
        raise NotImplementedError