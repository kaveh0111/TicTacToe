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
from Domain.gameEngine.events import GameEvent, TurnChanged
from Domain.gameEngine.events import *
from typing import List, Optional
from Application.AppObserver import Observer as AppObserver
from typing import List, Optional
from Domain.player.machineplayerstrategy.MachinePlayerStrategy import MachinePlayerStrategy
class GameType(Enum):
    SINGLE_PLAYER = 1
    TWO_PLAYER = 2

from typing import List, Optional


class GameApp(ABC):
    """Abstract base class for application"""
    def __init__(
        self,
        game_engine: GameEngine,
        player_list: List[Player],
        app_observer: Optional[AppObserver] = None,   # <— NEW param (optional to not break existing code)
    ) -> None:
        self._game_engine: GameEngine = game_engine
        self._player_list: List[Player] = player_list
        self._turn: Player = self._game_engine.getCurrentTurn()

        # store the dependency; if not provided, create a default one
        self._observer: AppObserver = app_observer if app_observer is not None else AppObserver()
        self._observer.subscribe(GameStarted, self.onGameStarted)
        self._observer.subscribe(MoveMade, self.onMoveMade)
        self._observer.subscribe(TurnChanged, self.onTurnChangedEvent)
        self._observer.subscribe(IlegalMove, self.onIlegalMove)
        self._observer.subscribe(TimerDeadline, self.onTimerDeadline)
        self._observer.subscribe(GameFinished, self.onGameFinished)
        self._observer.subscribe(GameOver, self.onGameOver)


    def getObserver(self) -> AppObserver:
        """
        Expose the application-level observer ot other modules
        so they can subscribe/unsubscribe directly.
        """
        return self._observer

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

    @abstractmethod
    def getPlayer(self, player_id: str) -> Optional[Player]:
        # it checks if the given Id is related to id of a game player, return its object, otherwise return None
        raise NotImplementedError

    @abstractmethod
    def onMove(self, player: Player, row: int, column: int) -> None:
        #here the game engine either accepted the move done by the user or
        #it give the result of the game done by one of the players (machine or other palyers in multiplayer games)
        #this function will call the client code GUI to update it (or later throw web API)
        raise NotImplementedError

    def onGameStarted(self, event: GameStarted) -> None:
        """Hook for GameStarted events."""
        pass

    def onMoveMade(self, event: MoveMade) -> None:
        """
        Hook for MoveMade events.
        Default: adapt to existing onMove(player, row, col).
        """
        player_obj = self.getPlayer(event.player)
        if player_obj is not None:
            self.onMove(player_obj, event.row, event.col)

    def onTurnChangedEvent(self, event: TurnChanged) -> None:
        """
        Hook for TurnChanged events.
        Default: if subclass defines onTurnChange(event), call it.
        """
        # We don't make onTurnChange abstract in base to avoid breaking subclasses.
        handler = getattr(self, "onTurnChange", None)
        if callable(handler):
            handler(event)

    def onIlegalMove(self, event: IlegalMove) -> None:
        """Hook for IlegalMove events."""
        pass

    def onTimerDeadline(self, event: TimerDeadline) -> None:
        """Hook for TimerDeadline events."""
        pass

    def onGameFinished(self, event: GameFinished) -> None:
        """Hook for GameFinished events."""
        pass

    def onGameOver(self, event: GameOver) -> None:
        """Hook for GameOver events."""
        pass
"""
    @abstractmethod
    def changeTurn(self, player: Player) -> None:
        #can be called with the callback from gameengine to change turn
        raise NotImplementedError
"""
"""
    @abstractmethod
    def onTurnChange(self, event: GameEvent) -> None:
        #callback for changing turns
        raise NotImplementedError
"""









class GameAppSinglePlayer(GameApp):
    """Implmentation  class for application"""
    def __init__(self, game_engine : GameEngine, player_list : List[Player]) -> None:
        super().__init__(game_engine, player_list)
        self._machine_player: MachinePlayer = None
        self._human_player: Player = None

        # checking exactly one machine and one human player is created
        if not self._player_list:
            raise AttributeError("GameApp: Player list is empty")

        for p in self._player_list:
            if isinstance(p, HumanPlayer):
                self._human_player = p
            if isinstance(p, MachinePlayer):
                self._machine_player = p

        if ((self._machine_player is None) or
                (self._human_player is None)):
            raise Exception('Invalid game type, GameApp requires one machine player and one human player')


    def onTurnChange(self, event: GameEvent) -> None:
        #callback for changing turns
        #inform subscribers
        #change the internal state for turning
        if not isinstance(event, TurnChanged):
            raise ValueError("GameAppSinglePlayer: TurnChanged, with wrong event type")
        new_player : Player = self.getPlayer(event.current_player)
        if new_player is None:
            raise ValueError("GameAppSinglePlayer: TurnChanged, with to an empty/or a new player not registered")
        self._turn = new_player

        # If it's the machine's turn, immediately ask for its move and execute it
        if new_player is self._machine_player:
            row, col = self._game_engine.getMachineMove()
            # This will again call acceptMove, check_finish, changeTurn, etc.
            self.executeMove(self._machine_player, row, col)
        else:
            # Human's turn: do nothing. GUI will call executeMove when the user clicks.
            pass



    def getPlayer(self, player_id: str) -> Optional[Player]:
        for p in self._player_list:
            if p.player_id == player_id:
                return p
        return None

    def executeMove(self, player: Player, row: int, column: int) -> None:
        print("I recived a move")
        self.isGamePlayer(player)

        if player is not self._turn:
            # Not this player's turn; ignore
            return

        print("sending the move to the game engine")
        if not self._game_engine.acceptMove(row, column, player):
            # invalid move (cell full etc.), you might notify UI and return
            return

        self._game_engine.check_finish()
        if not self._game_engine.isGameFinished():
            self._game_engine.changeTurn()

    def onMove(self, player: Player, row: int, column: int) -> None:
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

    def changeMachinePlayerStrategy(self, player: Player, new_strategy : MachinePlayerStrategy) -> None:
        #change the strategy of the machine player to change the dificulity levels of a single game etc.
        print("change the machine player strategy is not implmented yet")





    """
    def changeTurn(self, player: Player) -> None:
        #can be called with the callback from gameengine to change turn
        self.isGamePlayer(player)
        self._turn = player
    """
