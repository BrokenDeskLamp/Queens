import numpy as np
from queen import Queen


class Board:
    def __init__(self, n):
        self.n = n
        self.grid = np.zeros((n, n), dtype=int)
        self.queens = []

    def place_queens(self, queen_positions):
        """Place queens at specified positions."""
        self.queens = [Queen(x, y) for x, y in queen_positions]
        for q in self.queens:
            self.grid[q.x, q.y] = np.random.randint(1, 9)  # Assign random colors 1-8

    def spread_colors(self, strategy):
        """Spread colors according to a chosen strategy."""
        strategy(self.grid)

    def is_fully_colored(self):
        """Check if the board has no zero cells."""
        return np.all(self.grid > 0)
