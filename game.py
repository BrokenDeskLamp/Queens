import numpy as np
from board import Board


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

    def generate_random_board(self) -> Board:
        board = Board(self.board_size)
        num_regions = np.random.randint(2, self.board_size + 1)
        board.grid = np.random.randint(1, num_regions + 1, size=(self.board_size, self.board_size))
        return board

    def is_valid_move(self, board: Board, row: int, col: int, region_value: int) -> bool:
        # Implement actual rules here (one queen per row, column, region and non-adjacency).
        return True

    def evaluate_difficulty(self, board: Board) -> float:
        unique_regions, counts = np.unique(board.grid, return_counts=True)
        avg_size = counts.mean()
        std_size = counts.std()
        difficulty = std_size / (avg_size + 1e-5)
        return difficulty
