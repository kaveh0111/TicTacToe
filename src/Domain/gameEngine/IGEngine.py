"""
It is initiated by IGEngineFactory.py(its implmented class)
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




from abc import ABC, abstractmethod

class GameEngine(ABC):
    """Abstract game engine with lifecycle methods."""

    @abstractmethod
    def start(self) -> None:
        """Begin or resume the game."""
        raise NotImplementedError

    @abstractmethod
    def pause(self) -> None:
        """Pause the game."""
        raise NotImplementedError

    @abstractmethod
    def finish(self) -> None:
        """
        change the game over variable to true
        End the game and perform any cleanup."""
        raise NotImplementedError

    @abstractmethod
    def doMove(self) -> None:
        """HERE IT NEEDS TO INDICATE TEH PARAMETERS OF THE MOVE."""
        """THE human palyers will wait for the input from the user.
        the machine palyer will wait for the move from machine user."""
        raise NotImplementedError

    @abstractmethod
    def changeTurn(self) -> None:
        """It will change the turn to another player."""
        raise NotImplementedError

    """
    @abstractmethod
    def changeTurn(self) -> None:
        #It will change the turn to the given player.
        raise NotImplementedError
    """