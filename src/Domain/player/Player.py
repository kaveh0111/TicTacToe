from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple

from Domain.gameEngine import Board
from machineplayerstrategy.MachinePlayerStrategy import MachinePlayerStrategy
class PlayerType(Enum):
    HUMAN = 0
    COMPUTER = 1


class Player(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def play(self, board:Board = None) -> Tuple[int, int]:
        ...

    @abstractmethod
    def getPlayerType(self) -> PlayerType:
        ...


class HumanPlayer(Player):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._PlayerType = PlayerType.HUMAN

    def play(self, board:Board = None) -> Tuple[int, int]:
        print(f"{self.name} (human) plays their move.")

    def getPlayerType(self) -> PlayerType:
        return self._PlayerType


class MachinePlayer(Player):
    def __init__(self, name: str, strategy:MachinePlayerStrategy) -> None:
        super().__init__(name)
        self.__PlayerType = PlayerType.COMPUTER
        self.__strategy = strategy

    def play(self, board:Board = None) -> Tuple[int, int]:
        return_tuple = self.__strategy.play(board)
        print(f"{self.name} (CPU) calculates and plays a move.")
        return return_tuple

    def getPlayerType(self) -> PlayerType:
        return self.__PlayerType


if __name__ == "__main__":
    players: list[Player] = [HumanPlayer("Alex"), MachinePlayer("HAL")]
    for p in players:
        p.play()
