
from abc import ABC, abstractmethod
from enum import Enum
from Player import MachinePlayer, Player
from machineplayerstrategy.MachinePlayerStrategy import *

class MachinePlayerType(Enum):
    RANDOM = 1
    MINIMAX = 2


class MachinePlayerFactory(ABC):
    @abstractmethod
    def createPlayer(self, m_player_type : MachinePlayerType, num_rows : int = 3, num_cols : int = 3) -> Player:
        raise NotImplementedError


class RandomMachinePlayer(MachinePlayer):
    def createPlayer(self, m_player_type : MachinePlayerType, num_rows = 3, num_cols = 3) -> Player:
        match m_player_type:
            case MachinePlayerType.RANDOM:
                self.__strategy = RandomMachinePlayer(num_rows = num_rows, num_cols = num_cols)

            case MachinePlayerType.MINIMAX:
                self.__strategy = MinimaxPlayerStrategy(num_rows = num_rows, num_cols = num_cols)

            case _:
                raise ValueError("MachinePlayerFactory.py: Invalid player type")