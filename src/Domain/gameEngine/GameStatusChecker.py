from abc import ABC, abstractmethod

from Domain.gameEngine.Board import Board
from Domain.gameEngine.Cell import Cell

from dataclasses import dataclass
from typing import Optional, Any, List, Tuple


@dataclass
class GameResult:
    """
    Game evaluation result.
    """
    """
    finished: True  -> game over (win or draw)
    winner: whatever Cell stores, player_id
    """
    finished: bool
    winner: Optional[Any]
    winning_line_index: Optional[int] = None
    winning_cells: Optional[List[Tuple[int, int]]] = None


from abc import ABC, abstractmethod
from Domain.gameEngine.Board import Board


class GameStatusChecker(ABC):
    """
    Interface / base class for any game status checker.
    """

    @abstractmethod
    def evaluate(self, board: Board) -> GameResult:
        """
        Check the current game status for the given board and Returns:
            GameResult(finished, winner, winning_line_index, winning_cells)
        """
        raise NotImplementedError





class TicTacToeGameStatusChecker(GameStatusChecker):

    def _line_winner(self, cells: List[Cell]) -> Optional[Any]:
        """
        If all cells in the given line belong to the same non-empty player,
        return that player's id/sign.
        """
        first_owner: Optional[Any] = None

        for cell in cells:
            if cell.is_empty:
                return None

            owner = cell.get_current_user
            if first_owner is None:
                first_owner = owner
            elif owner != first_owner:
                # Different owner in the same line → not a winning line
                return None

        return first_owner

    def evaluate(self, board: Board) -> GameResult:

        cols = board._num_col
        rows = board._num_row

        line_index = 0

        #  Check all rows
        for row in range(rows):
            line = [board._grid[col][row] for col in range(cols)]
            winner = self._line_winner(line)
            if winner is not None:
                winning_cells = [(row, col) for col in range(cols)]
                return GameResult(
                    finished=True,
                    winner=winner,
                    winning_line_index=line_index,
                    winning_cells=winning_cells,
                )
            line_index += 1

        # Check all columns
        for col in range(cols):
            line = [board._grid[col][row] for row in range(rows)]
            winner = self._line_winner(line)
            if winner is not None:
                winning_cells = [(row, col) for row in range(rows)]
                return GameResult(
                    finished=True,
                    winner=winner,
                    winning_line_index=line_index,
                    winning_cells=winning_cells,
                )
            line_index += 1

        # Check diagonals  if board is square
        if cols == rows:
            main_diag = [board._grid[i][i] for i in range(cols)]
            winner = self._line_winner(main_diag)
            if winner is not None:
                winning_cells = [(i, i) for i in range(cols)]
                return GameResult(
                    finished=True,
                    winner=winner,
                    winning_line_index=line_index,  # rows + cols
                    winning_cells=winning_cells,
                )
            line_index += 1

            # anti-diagonal
            anti_diag = [board._grid[i][rows - 1 - i] for i in range(cols)]
            winner = self._line_winner(anti_diag)
            if winner is not None:
                winning_cells = [(i, rows - 1 - i) for i in range(cols)]
                return GameResult(
                    finished=True,
                    winner=winner,
                    winning_line_index=line_index,  # rows + cols + 1
                    winning_cells=winning_cells,
                )
            line_index += 1

        #No winner: check if there is any empty cell left
        for col in range(cols):
            for row in range(rows):
                if board._grid[col][row].is_empty:
                    # At least one empty cell → game still in progress
                    return GameResult(
                        finished=False,
                        winner=None,
                        winning_line_index=None,
                        winning_cells=None,
                    )

        # Board is full and no winner → draw
        return GameResult(
            finished=True,
            winner=None,
            winning_line_index=None,
            winning_cells=None,  # draw: no winning line
        )
