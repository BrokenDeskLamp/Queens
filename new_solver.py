from board import Board
import random
import numpy as np


def _backtrack(queen_placement: np.ndarray, grid: np.ndarray, row: int) -> True:
    n = queen_placement.shape[0]
    if row >= n:
        return True

    cols = list(range(n))
    random.shuffle(cols)
    for col in cols:
        if _is_valid_placement(queen_placement, row, col):
            queen_placement[row][col] = 1
            if _backtrack(queen_placement, row + 1):
                return True
            queen_placement[row][col] = 0

    return False


def _is_valid_placement(queen_placement: np.ndarray, grid: np.ndarray, row: int, col: int, colour: int) -> bool:
    check_colour = np.sum([queen_placement[i][j] for i, j in zip(*np.where(grid == colour))]) == 0

    check_queens = not (
        queen_placement[max(row - 1, 0) : row + 2, max(col - 1, 0) : col + 2].any()
        or queen_placement[row].any()
        or queen_placement[:, col].any()
    )

    return check_colour and check_queens


def unique_solution(queens_board: Board) -> bool:
    queen_placement = np.zeros((queens_board.n, queens_board.n), dtype=int)
    for queen in queens_board.queens:
        queen_placement[queen.x, queen.y] = 1

    grid = queens_board.grid.copy()
    found = _backtrack(queen_placement, grid, 0)
    return grid, found
