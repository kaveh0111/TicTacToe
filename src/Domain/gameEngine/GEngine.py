"""
It is initiated by GEngineFactory.py(its implmented class)
gameengine contains players, turning strategy, board (and cells inside it), winier checking,
move validation, a list of subcribers (UIs, voice, etc.)

It has states: Pause, Active,

It contains a player list.
It has a turning strategy
It has a subscribers module
It has a main loop.
"""

# Domain - Board & Cell
from Domain.gameEngine.GEObserver import Observer
from Domain.gameEngine.events import (GameEvent, MoveMade,
                                      TurnChanged, GameFinished)
from Domain.player.Player import Player, PlayerType
from Domain.gameEngine.GameStatusChecker import GameStatusChecker, TicTacToeGameStatusChecker, GameResult
# Domain - Strategy interface for machine players
from Domain.player.machineplayerstrategy.MachinePlayerStrategy import *
from typing import Optional, Tuple, List
from Domain.gameEngine.Board import Board
# Domain - Observer interface (UI/voice/logging subscribers implement this)
#from Domain.gameEngine.GEObserver import GEObserver
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class GameStatus(Enum):
    PLAYING = "PLAYING"
    FINISHED = "FINISHED"


class TurnStrategy:
    def __init__(self) -> None:
        self._current_player_idx: int = -1   # so first call gives index 0

    def getNextTurn(self, player_list: List[Player]) -> Player:
        assert player_list is not None, "TurnStrategy: player_list is None"
        assert len(player_list) == 2, "TurnStrategy: player_list should have 2 elements"

        self._current_player_idx = (self._current_player_idx + 1) % len(player_list)
        logger.debug(
            "TurnStrategy.getNextTurn() -> idx=%s, player=%s",
            self._current_player_idx,
            player_list[self._current_player_idx],
        )
        return player_list[self._current_player_idx]



from abc import ABC, abstractmethod

class GameEngine(ABC):
    """Abstract game engine with lifecycle methods."""
    def __init__(self, board: Board,
                 player_list : List[Player],
                 observer : Observer,
                 turn_strategy : TurnStrategy = None,
                 status_checker: GameStatusChecker = None) -> None:

        assert player_list is not None, "GameEngine: player_list is None"
        assert len(player_list) >= 2, "TurnStrategy: player_list has less than 2 elements"

        self._game_checker = status_checker
        if self._game_checker is None:
            self._game_checker = TicTacToeGameStatusChecker()
        self._turn_strategy = turn_strategy
        if self._turn_strategy is None:
            self._turn_strategy = TurnStrategy()

        assert board is not None, "GameEngine: board is None"

        assert observer is not None, "GameEngine: observer is None"

        self._player_list: List[Player] = player_list
        self._board: Board = board
        self._observer: Observer = observer
        self._winner : Optional[Player] = None
        self._winner_line = None
        self._current_turn: Player = self._turn_strategy.getNextTurn(self._player_list)

        logger.debug(
            "GameEngine.__init__(): board=%s, players=%s, current_turn=%s",
            board,
            player_list,
            self._current_turn,
        )

        self._observer.notify(
            TurnChanged(current_player=self._current_turn.player_id))


    def getCurrentTurn(self) -> Player:
        return self._current_turn

    @abstractmethod
    def setObserver(self, observer: Observer) -> None:
        raise NotImplementedError

    @abstractmethod
    def getObserver(self) -> Optional[Observer]:
        raise NotImplementedError

    @abstractmethod
    def setBoard(self, board:Board) -> None:
        raise NotImplementedError

    @abstractmethod
    def getBoard(self) -> Optional[Board]:
        raise NotImplementedError


    @abstractmethod
    def acceptMove(self, row:int, col:int, player : Player) -> bool:
        """if the move is accepted"""
        raise NotImplementedError


    @abstractmethod
    def isGameFinished(self) -> bool:
        #Pause the game.
        raise NotImplementedError

    @abstractmethod
    def changeTurn(self) -> None:
        """It will change the turn to another player."""
        raise NotImplementedError

    @abstractmethod
    def inform(self, event: GameEvent) -> None:
        raise NotImplementedError





class GameEngineImp(GameEngine):
    """Abstract game engine ."""
    def __init__(self,
                 board: Board,
                 player_list: List[Player],
                 observer: Observer,
                 turn_strategy: TurnStrategy = None,
                 status_checker: GameStatusChecker = None):
        super().__init__(board, player_list, observer, turn_strategy, status_checker)
        self._game_state = GameStatus.PLAYING

    def setObserver(self, observer: Observer) -> None:
        assert observer is not None, "GameEngine, setObserver: observer is None"
        self._observer = observer
        logger.debug("GameEngineImp.setObserver(): observer=%s", observer)

    def getObserver(self) -> Optional[Observer]:
        if self._observer is None:
            return None
        return self._observer


    def setBoard(self, board:Board) -> None:
        assert board is not None, "GameEngine, setBoard: board is None"
        self._board = board
        logger.debug("GameEngineImp.setBoard(): board=%s", board)


    def getBoard(self) -> Optional[Board]:
        if self._board is None:
            return None
        return self._board


    def isCellEmpty(self, row:int, col:int) -> bool:
        return self._board.isEmptyCell(row, col)


    def acceptMove(self, row:int, col:int, player : Player) -> bool:
        logger.debug("GameEngineImp.acceptMove(): player=%s, row=%s, col=%s", player, row, col)
        if not self._board.isEmptyCell(row, col):
            logger.debug("GameEngineImp.acceptMove(): cell (%s, %s) is full", row, col)
            return False
        self._board.selectCell(row, col, player.player_id)
        #self.inform()
        self._observer.notify(
            MoveMade(
                player_id=player.player_id,
                row=row,
                col=col,
                board_snapshot=self._board.get_snapshot()
            )
        )
        self.check_finish()
        if not self.isGameFinished():
            self.changeTurn()
        return True


    def isGameFinished(self) -> bool:
        if self._game_state == GameStatus.FINISHED:
            return True
        return False


    def check_finish(self):
        game_result: GameResult = self._game_checker.evaluate(self._board)
        logger.debug("GameEngineImp.check_finish(): result=%s", game_result)

        if not game_result.finished:
            return

        self._game_state = GameStatus.FINISHED

        if game_result.winner is None:
            # Draw: no winner
            self._winner = None
            self.inform(
                GameFinished(
                    winner_id=None,
                    winning_cells=game_result.winning_cells ))
            return

        # There is a winner
        self._winner = game_result.winner
        self.inform(
            GameFinished(
                winner_id=self._winner,
                winning_cells=game_result.winning_cells))

    def getMachineMove(self) -> Tuple[int, int]:
        """the machine player will wait for the move from machine user."""
        assert (
            self._current_turn.getPlayerType() is PlayerType.COMPUTER
        ), "Current turn player is not the computer player turn"
        logger.debug("GameEngineImp.getMachineMove(): current_turn=%s", self._current_turn)
        return self._current_turn.play(self._board)


    def changeTurn(self) -> None:
        self._current_turn = self._turn_strategy.getNextTurn(self._player_list)
        logger.debug("GameEngineImp.changeTurn(): new current_turn=%s", self._current_turn)
        self._observer.notify(
            TurnChanged(current_player=self._current_turn.player_id))



    def inform(self, event: GameEvent) -> None:
        logger.debug("GameEngineImp.inform(): event=%s", event)
        self._observer.notify(event)
