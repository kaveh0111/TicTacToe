"""
This is an interface class for implmenting Player.py for HumanPlayers
The concrete implmentation of it is required to be implmented.
"""

from abc import ABC, abstractmethod
from Player import HumanPlayer

class HumanPlayerFactory(ABC):
    @abstractmethod
    def createHumanPlayer(self, player_name : str) -> HumanPlayer:
        raise NotImplementedError()

class HumanPlayerFactImp(HumanPlayerFactory):
    def createHumanPlayer(self, player_name : str) -> HumanPlayer:
        return HumanPlayer(player_name)