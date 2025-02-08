import numpy as np
from queen import Queen
import random


class Board:
    def __init__(self, n: int):
        self.n = n
        self.grid = np.zeros((n, n), dtype=int)
        self.queens = []

    def place_queens(self, queen_positions: np.array):
        """Place queens at specified positions."""
        colours = list(range(1, self.n + 1))
        random.shuffle(colours)
        self.queens = [Queen(x, y, colour) for x, y, colour in zip(*np.where(queen_positions), colours)]
        for q in self.queens:
            self.grid[q.x, q.y] = q.colour

    def spread_colours(self, strategy):
        """Spread colors according to a chosen strategy."""
        while not self.is_fully_coloured():
            strategy(self.grid)

    def is_fully_coloured(self) -> bool:
        """Check if the board has no zero cells."""
        return np.all(self.grid > 0)
