"""It is an factory Interface for making the game, so it should be implmented in a child class

it should return IGameApp
It contains the parametrs used by the game engine and loading the UI
User account maangement and any other things may be added in the future
"""



from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Protocol, TypeVar, Optional
from GameApp import GameApp

# ---- Core domain protocols (no concrete implementations here) ----

class User(Protocol):
    """Marker protocol for a (human) user domain object."""
    ...


class MachineUser(Protocol):
    """Marker protocol for an automated/AI agent domain object."""
    ...


class GameEngine(Protocol):
    """Marker protocol for the core game engine object."""
    ...


class Interface(Protocol):
    """Protocol for something that can run the experience."""
    def run(self, engine: GameEngine, user: User, machine_user: MachineUser) -> None: ...
    # Feel free to extend with lifecycle hooks (start/stop) in concrete code.


# ---- Generic factory protocol ----

T = TypeVar("T")

class Factory(Protocol, Generic[T]):
    """A factory that knows how to construct a complex object."""
    def create(self) -> T: ...


# ---- Abstract Builder ----

class Builder(ABC):
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

    @property
    @abstractmethod
    def user_factory(self) -> Factory[User]:
        """Factory for creating the (human) User."""
        raise NotImplementedError

    @property
    @abstractmethod
    def machine_user_factory(self) -> Factory[MachineUser]:
        """Factory for creating the MachineUser (AI/agent)."""
        raise NotImplementedError

    @property
    @abstractmethod
    def game_engine_factory(self) -> Factory[GameEngine]:
        """Factory for creating the GameEngine."""
        raise NotImplementedError

    @property
    @abstractmethod
    def interface_factory(self) -> Factory[Interface]:
        """Factory for creating the Interface (CLI/GUI/Web/etc.)."""
        raise NotImplementedError

    # --- Internal state (populated by the template methods below) ---

    _user: Optional[User] = None
    _machine_user: Optional[MachineUser] = None
    _engine: Optional[GameEngine] = None
    _interface: Optional[Interface] = None

    # --- Template methods implementing the orchestration flow ---

    def set_user(self) -> User:
        """Create and store the User via its factory."""
        self._user = self.user_factory.create()
        return self._user

    def set_machine_user(self) -> MachineUser:
        """Create and store the MachineUser via its factory."""
        self._machine_user = self.machine_user_factory.create()
        return self._machine_user

    def init_game_engine(self) -> GameEngine:
        """Create and store the GameEngine via its factory."""
        self._engine = self.game_engine_factory.create()
        return self._engine

    def ensure_interface(self) -> Interface:
        """Lazily create and store the Interface via its factory."""
        if self._interface is None:
            self._interface = self.interface_factory.create()
        return self._interface

    def assemble(self) -> None:
        """
        Default assembly pipeline: create user, machine user, engine.
        Subclasses may override to change ordering or inject configuration.
        """
        if self._user is None:
            self.set_user()
        if self._machine_user is None:
            self.set_machine_user()
        if self._engine is None:
            self.init_game_engine()

    def run_interface(self) -> None:
        """
        Ensure everything is assembled, then run the interface with the
        engine, user, and machine user.
        """
        self.assemble()
        ui = self.ensure_interface()
        engine = self._require_engine()
        user = self._require_user()
        machine_user = self._require_machine_user()
        ui.run(engine, user, machine_user)

    # --- Helpers to assert presence of constructed parts ---

    def _require_user(self) -> User:
        if self._user is None:
            raise RuntimeError("User is not set. Call set_user() or assemble() first.")
        return self._user

    def _require_machine_user(self) -> MachineUser:
        if self._machine_user is None:
            raise RuntimeError("MachineUser is not set. Call set_machine_user() or assemble() first.")
        return self._machine_user

    def _require_engine(self) -> GameEngine:
        if self._engine is None:
            raise RuntimeError("GameEngine is not initialized. Call init_game_engine() or assemble() first.")
        return self._engine


# Optional: alias with lowercase name if you prefer to reference it as `builder`
builder = Builder
