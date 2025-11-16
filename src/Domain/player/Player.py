from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple
from dataclasses import dataclass
from Domain.gameEngine import Board

from Domain.player.machineplayerstrategy.MachinePlayerStrategy import (
    MachinePlayerStrategy,
    RandomPlayerStrategy,
)


class PlayerType(Enum):
    HUMAN = 0
    COMPUTER = 1


class PlayerSign(Enum):
    X = 0
    O = 1


class Player(ABC):
    def __init__(self, name: str, player_sign: PlayerSign) -> None:
        # store both name and sign (fixes bug #5)
        self.name = name
        self.__player_sign = player_sign

    @abstractmethod
    def play(self, board: Board) -> Tuple[int, int]:
        ...

    @abstractmethod
    def getPlayerType(self) -> PlayerType:
        ...

    @property
    def getPlayerSign(self) -> PlayerSign:
        return self.__player_sign


class HumanPlayer(Player):
    def __init__(self, name: str, player_sign: PlayerSign) -> None:
        # pass player_sign correctly to base (fixes bug #1)
        super().__init__(name, player_sign)
        self.__player_type = PlayerType.HUMAN

    def play(self, board: Board) -> Tuple[int, int]:
        # now returns a Tuple[int, int] (fixes bug #4)
        print(f"{self.name} (human) plays their move.")
        # TODO: replace with actual input/UI. Dummy move for now:
        return 0, 0

    def getPlayerType(self) -> PlayerType:
        # uses the existing attribute (fixes bug #3)
        return self.__player_type


class MachinePlayer(Player):
    def __init__(
        self,
        name: str,
        player_sign: PlayerSign,
        strategy: MachinePlayerStrategy = None) -> None:
        # pass player_sign correctly to base (fixes bug #1)
        super().__init__(name, player_sign)
        self.__player_type = PlayerType.COMPUTER
        if strategy is None:
            strategy = RandomPlayerStrategy(self)
            print("MachinePlayer, RandomPlayerStrategy Strategy created")

    def play(self, board: Board) -> Tuple[int, int]:
        if board is None:
            # Programming error: caller violated the contract
            raise ValueError("MachinePlayerStrategy: board must not be None")
        return_tuple = self.__strategy.play(board)
        print(f"{self.name} (CPU) calculates and plays a move.")
        return return_tuple

    def getPlayerType(self) -> PlayerType:
        return self.__player_type


if __name__ == "__main__":
    # call constructors with the required arguments (fixes bug #2)
    players: list[Player] = [
        HumanPlayer("Alex", PlayerSign.X),
        MachinePlayer("HAL", PlayerSign.O),
    ]
    for p in players:
        move = p.play(None)
        print(f"{p.name} played: {move}")
