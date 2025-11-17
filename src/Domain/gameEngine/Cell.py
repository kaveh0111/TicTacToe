""" It is used to represent a cell in a game engine """
from enum import Enum
from dataclasses import dataclass
from typing import Optional,Any

class CellStatus(Enum):
    EMPTY = 0
    SELECTED = 1


@dataclass
class Cell:

        _status : CellStatus = CellStatus.EMPTY
        _player_id : str = None

        @property
        def is_empty(self)->bool:
            if self._status is CellStatus.EMPTY:
                return True
            else:
                return False



        @property
        def status(self) -> CellStatus:
                return self._status

        @status.setter
        def status(self, value: CellStatus):
            self._status = value


        def select_cell(self, player_id: str):
            if self._status is not CellStatus.EMPTY:
                raise ValueError("The cell already selected")
            self._status = CellStatus.SELECTED
            self._player_id = player_id


        @property
        def get_current_user(self)->str:
            if self.status is CellStatus.EMPTY:
                raise ValueError("The cell is empty")
            return self._player_id

