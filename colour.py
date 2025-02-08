import numpy as np


class ColourSpread:
    @staticmethod
    def random_spread(grid):
        """Randomly spread a colour to an adjacent zero cell."""
        n = grid.shape[0]
        x, y = np.argwhere(grid > 0)[np.random.randint(len(np.argwhere(grid > 0)))]
        neighbours = [
            (x + dx, y + dy)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if 0 <= x + dx < n and 0 <= y + dy < n and grid[x + dx, y + dy] == 0
        ]
        if neighbours:
            nx, ny = neighbours[np.random.randint(len(neighbours))]
            grid[nx, ny] = grid[x, y]  # Spread the colour
