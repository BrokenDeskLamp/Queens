import pulp
import numpy as np
from board import Board


class QueensSolver:
    def __init__(self, queens_board: Board):
        self.board = queens_board.grid
        self.board_size = self.board.shape[0]
        given_sol = np.zeros((self.board_size, self.board_size), dtype=int)
        for queen in queens_board.queens:
            given_sol[queen.x, queen.y] = 1
        self.solutions = [given_sol]
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

    def prev_solution_constraints(self):
        return [
            pulp.lpSum([sol[i][j] for i in self.rows for j in self.cols if pulp.value(sol[i][j]) == 1])
            <= self.board_size - 1
            for sol in self.solutions
        ]

    def solve(self, max_solutions=1):
        self.create_problem()
        self.constraints = (
            self.row_constraints()
            + self.col_constraints()
            + self.colour_constraints()
            + self.adjacency_constraints()
            + self.zero_constraints()
            + self.prev_solution_constraints()
        )

        for constraint in self.constraints:
            self.prob += constraint
        for _ in range(max_solutions):
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
