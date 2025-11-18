"""It is an factory Interface for making the game, so it should be implmented in a child class

it should return IGameApp
It contains the parametrs used by the game engine and loading the UI
User account maangement and any other things may be added in the future
"""



from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Protocol, TypeVar, Optional, List

from Domain.gameEngine.GEngine import GameEngine
from Domain.gameEngine.GEngineFactory import GameEngineFactory
from Application.GameApp import GameApp, GameAppSinglePlayer
from Domain.player.Player import Player, HumanPlayer, MachinePlayer





# ---- Abstract Builder ----

class GameAppBuilder:
    """
    Abstract builder that orchestrates creation and wiring via factories.
    Responsibilities:
      - set_user(): create & store the User via its factory
      - set_machine_user(): create & store the MachineUser via its factory
      - init_game_engine(): create & store the GameEngine via its factory
      - run_interface(): create the Interface via its factory (if needed) and run it
                         with the engine, user, and machine user.

    Subclasses provide the concrete factories by implementing the abstract
    factory properties below.
    """

    # --- Factories to be supplied by subclasses ---

    # --- Internal state (populated by the template methods below) ---

    def getNewGameApp(self) -> GameApp:
        human_player : HumanPlayer = HumanPlayer( player_name="You")
        machine_player : MachinePlayer = MachinePlayer(player_name="Computer")
        players : List[Player] = [human_player, machine_player]
        game_engine : GameEngine = GameEngineFactory(players).getNewGameEngine()
        game_app: GameAppSinglePlayer = GameAppSinglePlayer(
            game_engine = game_engine,
            player_list=players)

        """
        Default assembly pipeline: create user, machine user, engine.
        Subclasses may override to change ordering or inject configuration.
        """
        return game_app


builder = GameAppBuilder().getNewGameApp()
