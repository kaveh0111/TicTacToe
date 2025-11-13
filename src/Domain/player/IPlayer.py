"""
The purpose of this file is to provide some basic interface for player
both the human and computer players inheritance from this class
It contains Play methods
for machine player it contains a strategy from IMachinePlayerStrategy class that implement how the oponent works
"""

from __future__ import annotations
from abc import ABC, abstractmethod


class Player(ABC):
    """Abstract player interface."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def play(self) -> None:
        """Perform this player's action."""
        raise NotImplementedError


class HumanPlayer(Player):
    def play(self) -> None:
        print(f"{self.name} (human) plays their move.")


class ComputerPlayer(Player):
    def play(self) -> None:
        print(f"{self.name} (CPU) calculates and plays a move.")


if __name__ == "__main__":
    players: list[Player] = [HumanPlayer("Alex"), ComputerPlayer("HAL")]
    for p in players:
        p.play()
