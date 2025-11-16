"""Configuration file"""
"""

  While the Singleton pattern is not ideal for long-term maintenance,  
it can still be useful for certain parts of the system, such as default values that must remain const during runtime.  
For example, the board size, which is currently fixed at 3×3.  
This does not impact unit testing because test modules can easily replace these values with integers  
without importing the Singleton class.
"""

from dataclasses import dataclass
from typing import Final

@dataclass(frozen=True)
class GameSettings:
    default_row_size: int = 3
    default_col_size: int = 3
    min_row_size: int = 3
    min_col_size: int = 3
    max_row_size: int = 3
    max_col_size: int = 3


SETTINGS: Final[GameSettings] = GameSettings()