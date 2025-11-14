"""
It is an application. its work is to run the gameengine
it checks a move is acceptable
It is a bridge between game engine and UI
One of its duties are to check if a move is acceptable(based on
            users turns, cell avalibility, row and column range, etc.)
"""

from abc import ABC, abstractmethod
from enum import Enum
from Domain.player.Player import Player
from Domain.gameEngine.GEngine import GameEngine

class GameType(Enum):
    SINGLE_PLAYER = 1
    TWO_PLAYER = 2


class GameApp(ABC):
    """Abstract base class for application"""
    def __init__(self, game_engine : GameEngine) -> None:

    @abstractmethod
    def moveFromUser(self, player: Player, row : int, column : int) -> None:
        #check if move is legit
        #then send it to the game_engine
        raise NotImplementedError

    def performedMove(self, player: Player, row: int, column: int) -> None:
        #here the game engine either accepted the move done by the user or
        #it give the result of the game done by one of the players (machine or other palyers in multiplayer games)
        #this function will call the client code GUI to update it (or later throw web API)
        raise NotImplementedError