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
        board = QueensBoard(self.board_size)
        board.grid = np.random.randint(1, self.board_size + 1, (self.board_size, self.board_size))
        return board


# test = QueensGame(8)
# b = test.generate_random_board()
# print("Done!")
