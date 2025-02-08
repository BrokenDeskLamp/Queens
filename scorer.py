from solver import QueensSolver
from board import Board
from new_solver import unique_solution


class Scorer:
    @staticmethod
    def evaluate_board(board: Board) -> float:
        """Evaluate board based on complexity and uniqueness."""
        solver = QueensSolver(board)
        solver.solve(6)
        num_solutions = solver.num_solutions
        return num_solutions

    @staticmethod
    def evaluate_board_fast(board: Board) -> float:
        """Evaluate board based on complexity and uniqueness."""
        unique_sol = unique_solution(board)
        return 1 if unique_sol else 2
