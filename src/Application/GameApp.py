"""
It is an application. its work is to run the gameengine
it checks a move is acceptable
It is a bridge between game engine and UI or
One of its duties are to check if a move is acceptable(based on
            users turns, cell avalibility, row and column range, etc.)
"""

from abc import ABC, abstractmethod
from enum import Enum
from Domain.player.Player import Player, HumanPlayer, MachinePlayer
from Domain.gameEngine.GEngine import GameEngine
from Domain.gameEngine.events import GameEvent
from Domain.gameEngine.observer import Observer
from typing import List
from Domain.player.machineplayerstrategy.MachinePlayerStrategy import MachinePlayerStrategy
class GameType(Enum):
    SINGLE_PLAYER = 1
    TWO_PLAYER = 2


class GameApp(ABC):
    """Abstract base class for application"""
    def __init__(self, game_engine : GameEngine, player_list : List[Player]) -> None:
        self._game_engine : GameEngine = game_engine
        self._player_list : List[Player] = player_list
        self._turn: Player = None

    @abstractmethod
    def changeMachinePlayerStrategy(self, player: Player, new_strategy : MachinePlayerStrategy) -> None:
        #change the strategy of the machine player to change the dificulity levels of a single game etc.
        raise NotImplementedError


    @abstractmethod
    def executeMove(self, player: Player, row : int, column : int) -> None:
        #check if move is legit users turn and empty cell
        #then send it to the game_engine
        raise NotImplementedError

    @abstractmethod
    def isGamePlayer(self, player: Player) -> bool:
        #it checks if the given player is playing in the game
        raise NotImplementedError

    def performedMove(self, player: Player, row: int, column: int) -> None:
        #here the game engine either accepted the move done by the user or
        #it give the result of the game done by one of the players (machine or other palyers in multiplayer games)
        #this function will call the client code GUI to update it (or later throw web API)
        raise NotImplementedError

    @abstractmethod
    def changeTurn(self, player: Player) -> None:
        #can be called with the callback from gameengine to change turn
        raise NotImplementedError

    @abstractmethod
    def onChangeTurn(self, event: GameEvent) -> None:
        #callback for changing turns
        raise NotImplementedError









class GameAppSinglePlayer(GameApp):
    """Implmentation  class for application"""
    def __init__(self, game_engine : GameEngine, player_list : List[Player]) -> None:
        super().__init__(game_engine, player_list)
        self._machine_player: MachinePlayer = None
        self._human_player: Player = None

        # checking exactly one machine and one human player is created
        if self._player_list is None:
            raise AttributeError("GameApp: Player list is empty")

        for p in self._player_list:
            if isinstance(p, HumanPlayer):
                self._human_player = p
            if isinstance(p, MachinePlayer):
                self._machine_player = p

        if ((self._machine_player is None) or
                (self._human_player is None)):
            raise Exception('Invalid game type, GameApp requires one machine player and one human player')


    def onChangeTurn(self, event: GameEvent) -> None:
        #callback for changing turns
        raise NotImplementedError


    def executeMove(self, player: Player, row : int, column : int) -> None:
        self.isGamePlayer(player)
        #if player is self._machine_player:
        #    raise AttributeError("GameAppSinglePlayer Error: The machine player cannot work as a human player")
        if not player is self._turn:
            return
        print("sending the move to the game engine")
        self._game_engine.acceptMove(row, column, player)
        self._game_engine.check_finish()
        self._game_engine.changeTurn()




    def performedMove(self, player: Player, row: int, column: int) -> None:
        #here the game engine either accepted the move done by the user or
        #it give the result of the game done by one of the players (machine or other palyers in multiplayer games)
        #this function will call the client code GUI to update it (or later throw web API)
        raise NotImplementedError

    def isGamePlayer(self, player: Player) -> bool:
        if player is None:
            raise AttributeError("GameAppSinglePlayer: The player  is empty")
        if not any(player is x for x in self._player_list):
            raise AttributeError("GameAppSinglePlayer: Player is not in current player list")
        return True



    def changeTurn(self, player: Player) -> None:
        #can be called with the callback from gameengine to change turn
        self.isGamePlayer(player)
        self._turn = player
