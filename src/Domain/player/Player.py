from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple, Optional
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
    _next_id: int = 0   # <--- class-level counter shared by all players

    def __init__(self, player_name: Optional[str]) -> None:
        # unique id per Player instance
        self._player_id = Player._next_id
        Player._next_id += 1

        # existing fields
        self._player_name = player_name

    @abstractmethod
    def play(self, board: Board) -> Tuple[int, int]:
        ...

    @abstractmethod
    def getPlayerType(self) -> PlayerType:
        ...

    @property
    def getPlayerName(self) -> str:
        return self._player_name

    @property
    def player_id(self) -> int:
        """Read-only unique id for this player."""
        return self._player_id


class HumanPlayer(Player):
    def __init__(self, player_name: Optional[str]) -> None:
        super().__init__(player_name)
        self.__player_type = PlayerType.HUMAN


    def play(self, board: Board) -> Tuple[int, int]:
        # now returns a Tuple[int, int] (fixes bug #4)
        print(f"{self.getPlayerName} (human) plays their move.")
        # TODO: replace with actual input/UI. Dummy move for now:
        return 0, 0

    def getPlayerType(self) -> PlayerType:
        # uses the existing attribute (fixes bug #3)
        return self.__player_type


class MachinePlayer(Player):

    def __init__(
            self,
            player_name: Optional[str],
            strategy: Optional[MachinePlayerStrategy] = None
    ) -> None:
        super().__init__(player_name)
        self.__player_type = PlayerType.COMPUTER
        if strategy is None:
            self._strategy = RandomPlayerStrategy()  # depending on its ctor
        else:
            self._strategy = strategy

    def play(self, board: Board) -> Tuple[int, int]:
        if board is None:
            # Programming error: caller violated the contract
            raise ValueError("MachinePlayerStrategy: board must not be None")
        return_tuple : Tuple[int, int] = self._strategy.play(board)
        print(f"{self.name} (CPU) calculates and plays a move.")
        return return_tuple

    def getPlayerType(self) -> PlayerType:
        return self.__player_type


if __name__ == "__main__":
    # call constructors with the required arguments (fixes bug #2)
    players: list[Player] = [
        HumanPlayer("Alex"),
        MachinePlayer("HAL"),
    ]
    for p in players:
        #move = p.play(None)
        print(f"{p.getPlayerName} played: ")
