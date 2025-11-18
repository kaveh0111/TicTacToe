"""It is called to make the game engine factory

gameengine contains players, turning strategy, board (and cells inside it),
 winier checking, move validation, a list of subcribers (UIs, voice, etc.)
"""
from Domain.gameEngine.Board import Board
from Domain.gameEngine.GEObserver import Observer
from Domain.gameEngine.GEngine import GameEngine, GameEngineImp
from Infrastructure.Configuration import SETTINGS
from Domain.player.Player import Player
from typing import List

class GameEngineFactory:
    def __init__(self, player_list : List[Player]) -> None:
        self._row_size = SETTINGS.default_row_size
        self._col_size = SETTINGS.default_col_size
        self._player_list: List[Player] = player_list

        #set turn_strategy : or let it be default
        #set status_checker or let it be the default
        #call the gameengine and return it.

    def getNewGameEngine(self) -> GameEngine:
        board: Board = Board(num_row=self._row_size, num_col=self._col_size)
        game_engine_observer: Observer = Observer()
        game_engine : GameEngine = GameEngineImp(board = board,
                                                    player_list = self._player_list,
                                                    observer = game_engine_observer)
        return game_engine
