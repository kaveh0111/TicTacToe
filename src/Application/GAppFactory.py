"""It is an factory Interface for making the game, so it should be implmented in a child class

it should return IGameApp
It contains the parametrs used by the game engine and loading the UI
User account maangement and any other things may be added in the future
"""



from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Protocol, TypeVar, Optional, List
import logging

from Domain.gameEngine.GEngine import GameEngine
from Domain.gameEngine.GEngineFactory import GameEngineFactory
from Application.GameApp import GameApp, GameAppSinglePlayer
from Domain.player.Player import Player, HumanPlayer, MachinePlayer


logger = logging.getLogger(__name__)



# ---- Abstract Builder ----

class GameAppBuilder:
    """
    Abstract builder that orchestrates creation and wiring via factories.
    Responsibilities:
      - set_user(): create & store the User via its factory
      - set_machine_user(): create & store the MachineUser via its factory
      - init_game_engine(): create & store the GameEngine via its factory
      - run_interface():  run it with the engine, user, and machine user.

    Subclasses provide the concrete factories by implementing the abstract
    factory properties below.
    """
    def __init__(self):
        self._human_player: Optional[HumanPlayer] = None
        self._machine_player: Optional[MachinePlayer] = None
        self._game_app: Optional[GameApp] = None

    # --- Internal state (populated by the template methods below) ---

    def getNewGameApp(self) -> GameApp:
        logger.debug("GameAppBuilder.getNewGameApp() called: creating players and game engine.")
        self._human_player = HumanPlayer(player_name="You")
        self._machine_player = MachinePlayer(player_name="Computer")
        players: List[Player] = [self._human_player, self._machine_player]

        game_engine: GameEngine = GameEngineFactory(players).getNewGameEngine()
        game_app: GameAppSinglePlayer = GameAppSinglePlayer(
            game_engine=game_engine,
            player_list=players)

        logger.debug(
            "GameAppBuilder.getNewGameApp() created GameAppSinglePlayer with human=%s, machine=%s",
            self._human_player,
            self._machine_player,
        )

        """
        Default assembly pipeline: create user, machine user, engine.
        Subclasses may override to change ordering or inject configuration.
        """
        return game_app

    def get_human_player_name_id(self) -> tuple[str, int]:
        """
        Returns (name, id) for the human player created in getNewGameApp().
        """
        assert self._human_player is not None, "GameAppBuilder: getNewGameApp() has not been called yet."
        # Accessing protected attributes to avoid changing the Player class.
        logger.debug(
            "GameAppBuilder.get_human_player_name_id() -> (%s, %s)",
            self._human_player.getPlayerName,
            self._human_player.player_id,
        )
        return self._human_player.getPlayerName, self._human_player.player_id

    def get_machine_player_name_id(self) -> tuple[str, int]:
        """
        Returns (name, id) for the machine player created in getNewGameApp().
        """
        assert self._machine_player is not None, "GameAppBuilder: getNewGameApp() has not been called yet."
        logger.debug(
            "GameAppBuilder.get_machine_player_name_id() -> (%s, %s)",
            self._machine_player.getPlayerName,
            self._machine_player.player_id,
        )
        return self._machine_player.getPlayerName, self._machine_player.player_id

    def setup_ui_players(self, window) -> None:

        #Configure the UI with the human and machine player's name/id.

        # ensure players are created
        assert (
            self._human_player is not None and self._machine_player is not None
        ), "GameAppBuilder: call getNewGameApp() before setup_ui_players()."

        human_name, human_id = self.get_human_player_name_id()
        machine_name, machine_id = self.get_machine_player_name_id()

        logger.debug(
            "GameAppBuilder.setup_ui_players(): configuring UI with human(id=%s, name=%s) "
            "and machine(id=%s, name=%s)",
            human_id,
            human_name,
            machine_id,
            machine_name,
        )

        window.setMyPlayer(human_id, human_name)
        window.setOpponent(machine_id, machine_name)

    def build_and_bind_game(self, window) -> GameApp:
        """
        Create a fresh GameApp and connect it to the given UI window
        """
        logger.debug("GameAppBuilder.build_and_bind_game() called.")
        game_app = self.getNewGameApp()
        window.setGameApp(game_app)
        self.setup_ui_players(window)
        logger.debug("GameAppBuilder.build_and_bind_game() completed.")
        return game_app
