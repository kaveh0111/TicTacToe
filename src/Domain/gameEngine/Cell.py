""" It is used to represent a cell in a game engine """
from dataclasses import dataclass

@dataclass
class Cell:
    __col: int
    __row: int
    _is_selected: bool = False

    @property
    def col(self):
        return self.__col

    @col.setter
    def col(self, col: int):
        self.__col = col

    @property
    def row(self):
        return self.__row

    @row.setter
    def row(self, row: int):
        self.__row = row

    @property
    def is_selected(self):
        return self._is_selected

    @is_selected.setter
    def is_selected(self, is_selected: bool = True):
        self._is_selected = is_selected

