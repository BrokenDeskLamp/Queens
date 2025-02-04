import numpy as np


class Board:
    """A generic puzzle board representation."""

    def __init__(self, board_size: int):
        self.board_size = board_size
        self.grid = np.zeros((board_size, board_size), dtype=int)

    def display(self):
        """Display the board."""
        print(self.grid)

    def clone(self):
        """Return a deep copy of the board."""
        new_board = Board(self.board_size)
        new_board.grid = self.grid.copy()
        return new_board
