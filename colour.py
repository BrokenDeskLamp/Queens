import numpy as np


class ColourSpread:
    @staticmethod
    def random_spread(grid):
        """Randomly spread colours to adjacent zero cells."""
        n = grid.shape[0]
        while np.any(grid == 0):
            x, y = np.argwhere(grid > 0)[np.random.randint(len(np.argwhere(grid > 0)))]
            neighbors = [
                (x + dx, y + dy)
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if 0 <= x + dx < n and 0 <= y + dy < n and grid[x + dx, y + dy] == 0
            ]
            if neighbors:
                nx, ny = neighbors[np.random.randint(len(neighbors))]
                grid[nx, ny] = grid[x, y]  # Spread the colour
