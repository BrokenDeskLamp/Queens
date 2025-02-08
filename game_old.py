import random

import numpy as np

from board import Board, QueensBoard


class Game:
    """Abstract base class for a puzzle game."""

    def __init__(self, board_size: int):
        self.board_size = board_size

    def generate_random_board(self) -> Board:
        raise NotImplementedError

    def is_valid_move(self, board: Board, row: int, col: int, value: int) -> bool:
        raise NotImplementedError

    def evaluate_difficulty(self, board: Board) -> float:
        raise NotImplementedError


class QueensGame(Game):
    """Concrete implementation of the Queens puzzle."""

    def __init__(self, board_size: int):
        super().__init__(board_size)

    def generate_random_board(self) -> QueensBoard:
        board = self.initialise_board()
        while np.isin(0, board.grid):
            pass
        return board

    def initialise_board(self) -> QueensBoard:
        """Initialises an uncoloured board and randomly places queens in a valid configuration"""
        board = QueensBoard(self.board_size)
        self._placed = False
        self._backtrack(board, 0)
        return board

    def _backtrack(self, board: QueensBoard, row: int):
        if row == board.board_size:
            self._placed = True
            return

        cols = list(range(self.board_size))
        random.shuffle(cols)
        for col in cols:
            if self.is_valid_move(board, row, col):
                original = board.queens[row, col]
                board.queens[row, col] = 1
                self._backtrack(board, row + 1)
                if self._placed:
                    return
                board.queens[row, col] = original

    def is_valid_move(self, board: QueensBoard, row: int, col: int) -> bool:
        return not (
            board.queens[max(row - 1, 0) : row + 2, max(col - 1, 0) : col + 2].any()
            or board.queens[row].any()
            or board.queens[:, col].any()
        )

    def evaluate_difficulty(self, board: QueensBoard) -> float:
        unique_regions, counts = np.unique(board.grid, return_counts=True)
        avg_size = counts.mean()
        std_size = counts.std()
        difficulty = std_size / (avg_size + 1e-5)
        return difficulty


test = QueensGame(8)
b = test.initialise_board()
print("Done!")
