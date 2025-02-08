import random
import numpy as np


def _backtrack(grid: np.array, row: int) -> True:
    n = grid.shape[0]
    if row >= n:
        return True

    cols = list(range(n))
    random.shuffle(cols)
    for col in cols:
        if _is_valid_placement(grid, row, col):
            grid[row][col] = 1
            if _backtrack(grid, row + 1):
                return True
            grid[row][col] = 0

    return False


def _is_valid_placement(grid: np.array, row: int, col: int) -> bool:
    return not (
        grid[max(row - 1, 0) : row + 2, max(col - 1, 0) : col + 2].any() or grid[row].any() or grid[:, col].any()
    )


def generate_queen_positions(n: int) -> np.array:
    """Generate a valid N-Queens solution."""
    grid = np.zeros((n, n))
    _backtrack(grid, 0)
    return grid
