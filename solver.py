from board import Board
from game import Game
import pulp
import numpy as np


class Solver:
    """Backtracking solver to count or find solutions."""

    def __init__(self, game: Game):
        self.game = game
        self.solution_count = 0

    def solve(self, board: Board, max_count: int = 2) -> int:
        self.solution_count = 0
        self._backtrack(board, 0, max_count)
        return self.solution_count

    def _backtrack(self, board: Board, row: int, max_count: int):
        if row == board.board_size:
            self.solution_count += 1
            return

        for col in range(board.board_size):
            if self.game.is_valid_move(board, row, col, board.grid[row, col]):
                original = board.grid[row, col]
                board.grid[row, col] = 1  # Assume 1 means a queen is placed.
                self._backtrack(board, row + 1, max_count)
                if self.solution_count >= max_count:
                    return
                board.grid[row, col] = original


class QueensSolver:
    def __init__(self, board: np.array):
        self.board = board
        self.board_size = board.shape[0]
        self.solutions = []
        self.colours = list(range(1, self.board_size + 1))
        self.rows = self.cols = range(self.board_size)

    def create_problem(self):
        self.prob = pulp.LpProblem("Queens", pulp.LpMinimize)
        self.choices = pulp.LpVariable.dicts(name="Queen", indices=(self.rows, self.cols), cat="Binary")
        self.constraints = []

    def row_constraints(self):
        return [pulp.lpSum([self.choices[r][c] for r in self.rows]) == 1 for c in self.cols]

    def col_constraints(self):
        return [pulp.lpSum([self.choices[r][c] for c in self.cols]) == 1 for r in self.rows]

    def colour_constraints(self):
        return [
            pulp.lpSum([self.choices[i][j] for i, j in zip(*np.where(self.board == colour))]) == 1
            for colour in self.colours
        ]

    def adjacent_indices(self):
        return {
            frozenset([(x, y), (x + dx, y + dy)])
            for x in self.rows
            for y in self.cols
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
            if (not dx == dy == 0) and x + dx in self.rows and y + dy in self.cols
        }

    def adjacency_constraints(self):
        return [self.choices[i][j] + self.choices[k][l] <= 1 for (i, j), (k, l) in self.adjacent_indices()]

    def zero_constraints(self):
        return [self.choices[i][j] == 0 for i in self.rows for j in self.cols if self.board[i][j] == 0]

    def solve(self):
        self.create_problem()
        self.constraints = (
            self.row_constraints()
            + self.col_constraints()
            + self.colour_constraints()
            + self.adjacency_constraints()
            + self.zero_constraints()
        )
        for constraint in self.constraints:
            self.prob += constraint
        self.solutions = []
        for _ in range(100):
            self.prob.solve(pulp.PULP_CBC_CMD(msg=False))
            if self.prob.status != 1:
                break
            self.solutions.append(np.array([[pulp.value(self.choices[i][j]) for j in self.cols] for i in self.rows]))
            self.prob += (
                pulp.lpSum(
                    [self.choices[i][j] for i in self.rows for j in self.cols if pulp.value(self.choices[i][j]) == 1]
                )
                <= len(self.rows) - 1
            )

        self.num_solutions = len(self.solutions)


# board = np.array([[0, 1, 1, 1], [4, 2, 1, 1], [4, 2, 3, 3], [2, 2, 2, 2]])
# n = 8
# board = np.random.randint(1, n + 1, (n, n))
# solver = QueensSolver(board)
# solver.solve()
# print("Done!")
