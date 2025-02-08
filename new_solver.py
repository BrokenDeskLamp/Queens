from board import Board
import numpy as np


def _backtrack(queens_placement: np.ndarray, grid: np.ndarray, known_solution: np.ndarray, row: int) -> True:
    n = queens_placement.shape[0]
    if row >= n:
        return True

    for col in range(n):
        if _is_valid_placement(queens_placement, grid, known_solution, row, col):
            queens_placement[row][col] = 1
            if _backtrack(queens_placement, grid, known_solution, row + 1):
                return True
            queens_placement[row][col] = 0
    return False


def _is_valid_placement(
    queens_placement: np.ndarray, grid: np.ndarray, known_solution: np.ndarray, row: int, col: int
) -> bool:
    colour = grid[row][col]
    check_colour = np.sum([queens_placement[i][j] for i, j in zip(*np.where(grid == colour))]) == 0

    check_queens = not (
        queens_placement[max(row - 1, 0) : row + 2, max(col - 1, 0) : col + 2].any()
        or queens_placement[row].any()
        or queens_placement[:, col].any()
    )

    new_placement = queens_placement.copy()
    new_placement[row][col] = 1
    check_not_known = not np.array_equal(new_placement, known_solution)

    return check_colour and check_queens and check_not_known


def unique_solution(queens_board: Board) -> np.array:
    queens_placement = np.zeros((queens_board.n, queens_board.n), dtype=int)
    known_solution = np.zeros((queens_board.n, queens_board.n), dtype=int)
    for queen in queens_board.queens:
        known_solution[queen.x, queen.y] = 1
    grid = queens_board.grid.copy()
    found = _backtrack(queens_placement, grid, known_solution, 0)
    return not found
