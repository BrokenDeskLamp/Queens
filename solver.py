from board import Board
from game import Game


class Solver:
    """Backtracking solver to count or find solutions."""

    def __init__(self, game: Game):
        self.game = game
        self.solution_count = 0

    def solve(self, board: Board, max_count: int = 2) -> int:
        self.solution_count = 0
        self._backtrack(board, 0, max_count)
        return self.solution_count

    def _backtrack(self, board: Board, row: int, max_count: int):
        if row == board.board_size:
            self.solution_count += 1
            return

        for col in range(board.board_size):
            if self.game.is_valid_move(board, row, col, board.grid[row, col]):
                original = board.grid[row, col]
                board.grid[row, col] = 1  # Assume 1 means a queen is placed.
                self._backtrack(board, row + 1, max_count)
                if self.solution_count >= max_count:
                    return
                board.grid[row, col] = original
