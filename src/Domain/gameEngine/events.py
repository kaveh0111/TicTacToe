
from __future__ import annotations
from typing import Protocol, List, Optional

from typing import Callable, Dict, List, Type
from dataclasses import dataclass


#base event class
@dataclass
class GameEvent:
    pass


@dataclass
class GameStarted(GameEvent):
    player: list[str]

@dataclass
class TimerDeadline(GameEvent):
    player: str


@dataclass
class IlegalMove(GameEvent):
    player: str
    row: int
    col: int

@dataclass
class MoveMade(GameEvent):
    player: str
    row: int
    col: int
    board_snapshot: list[list[str]]


@dataclass
class TurnChanged(GameEvent):
    current_player: str


@dataclass
class GameOver(GameEvent):
    winner: Optional[str]  # None = draw
    board_snapshot: list[list[str]]

    ...
