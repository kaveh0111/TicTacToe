"""
It is initiated by GEngineFactory.py(its implmented class)
gameengine contains players, turning strategy, board (and cells inside it), winier checking,
move validation, a list of subcribers (UIs, voice, etc.)

It has states: Pause, Active,

It contains a player list.
It has a turning strategy
It has a subscribers module
It has a main loop.

Its main loop is like:
while (not is_finished)
    user turn
    user getNextMove
    is_finished GameWin;
    Subscribers.inform();

delete everything to prepare for the next


"""

# Domain - Board & Cell
from Domain.gameEngine.Board import Board
from Domain.gameEngine.Cell import Cell
from Domain.gameEngine.observer import Observer
from Domain.gameEngine.events import GameEvent, TurnChanged
from Domain.player.Player import Player, PlayerType

# Domain - Strategy interface for machine players
from Domain.player.machineplayerstrategy.MachinePlayerStrategy import *
from typing import Optional, Tuple
# Domain - Observer interface (UI/voice/logging subscribers implement this)
#from Domain.gameEngine.GEObserver import GEObserver
from enum import Enum

class GameStatus(Enum):
    PLAYING = "PLAYING"
    FINISHED = "FINISHED"


class TurnStrategy:
    _current_player_idx: int = 1

    def getNextTurn(self, player_list : List[Player]) -> Player:
        if player_list is None:
            raise ValueError("TurnStrategy: player_list is None")
        if len(player_list) != 2:
            raise ValueError("TurnStrategy: player_list should have 2 elements")

        self._current_player_idx -= 1
        return player_list[self._current_player_idx]



from abc import ABC, abstractmethod

class GameEngine(ABC):
    """Abstract game engine with lifecycle methods."""
    def __init__(self, board: Board,
                 player_list : List[Player],
                 observer : Observer,
                 turn_strategy : TurnStrategy = None) -> None:

        if player_list is None:
            raise ValueError("GameEngine: player_list is None")
        if len(player_list) < 2:
            raise ValueError("TurnStrategy: player_list has less than 2 elements")

        self._turn_strategy = turn_strategy
        if self._turn_strategy is None:
            self._turn_strategy = TurnStrategy()

        if board is None:
            raise ValueError("GameEngine: board is None")

        if observer is None:
            raise ValueError("GameEngine: observer is None")

        self._player_list: List[Player] = player_list
        self._current_turn : Player = self._turn_strategy.getNextTurn(self._player_list)
        self._board: Board = board
        self._observer: Observer = observer

    @abstractmethod
    def setObserver(self, observer: Observer) -> None:
        raise NotImplementedError

    @abstractmethod
    def getObserver(self) -> Optional[Observer]:
        raise NotImplementedError

    def setBoard(self, board:Board) -> None:
        raise NotImplementedError

    @abstractmethod
    def getBoard(self) -> Optional[Board]:
        raise NotImplementedError


    @abstractmethod
    def acceptMove(self, row:int, col:int, player : Player) -> bool:
        """if the move is accepted, return row and col else return None"""
        raise NotImplementedError

    @abstractmethod
    def isGameFinished(self) -> bool:
        """Pause the game."""
        raise NotImplementedError

    def getWinner(self) -> Optional[Player]:
        #first check if the game is finished, then return None or the player game
        raise NotImplementedError

    @abstractmethod
    def finish(self) -> None:
        """
        clear the game board."""
        raise NotImplementedError

    @abstractmethod
    def getNextMove(self) -> None:
        """HERE IT NEEDS TO INDICATE TEH PARAMETERS OF THE MOVE."""
        """THE human palyers will wait for the input from the user.
        the machine palyer will wait for the move from machine user."""
        raise NotImplementedError

    @abstractmethod
    def changeTurn(self) -> None:
        """It will change the turn to another player."""
        raise NotImplementedError

    @abstractmethod
    def addObserver(self, observer : Observer) -> None:
        #accept the observer class for notifications
        raise NotImplementedError

    @abstractmethod
    def inform(self, envent: GameEvent) -> None:
        raise NotImplementedError








class GameEngineImp(GameEngine):
    """Abstract game engine with lifecycle methods."""
    def __init__(self):
        super().__init__()
        self._game_state : GameStatus = GameStatus.PLAYING

    def setObserver(self, observer: Observer) -> None:
        if observer is None:
            raise ValueError("GameEngine, setObserver: observer is None")
        self._observer = observer

    def getObserver(self) -> Optional[Observer]:
        if self._observer is None:
            return None
        return self._observer


    def setBoard(self, board:Board) -> None:
        if board is None:
            raise ValueError("GameEngine, setBoard: board is None")
        self._board = board


    def getBoard(self) -> Optional[Board]:
        if self._board is None:
            return None
        return self._board


    def isCellEmpty(self, row:int, col:int) -> bool:
        return self._board.isEmptyCell(row, col)


    def acceptMove(self, row:int, col:int, player : Player) -> bool:
        if not self._board.isEmptyCell(col, row):
            return False
        self._board.selectCell(row, col, str(player.player_id))
        #self.inform()
        return True


    def isGameFinished(self) -> bool:
        if self._game_state == GameStatus.FINISHED:
            return True
        return False


    def getWinner(self) -> Optional[Player]:
        #first check if the game is finished, then return None or the player game
        raise NotImplementedError

    def finish(self) -> None:
        """
        clear the game board."""
        raise NotImplementedError

    def getNextMove(self) -> None:
        """the machine player will wait for the move from machine user."""
        if not (self._current_turn.getPlayerType() is PlayerType.COMPUTER):
            raise ValueError("Current turn player is not the computer player turn")

        self._current_turn.play(self._board)


        raise NotImplementedError

    def changeTurn(self) -> None:
        self._turn_strategy.getNextTurn(self._player_list)
        self._observer.notify(TurnChanged(current_player=str(self._current_turn.player_id)))
        #notify subscribers


    def inform(self, event: GameEvent) -> None:
        self._observer.notify(event)





