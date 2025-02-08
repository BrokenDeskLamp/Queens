from solver import QueensSolver
from board import Board


class Scorer:
    @staticmethod
    def evaluate_board(board: Board) -> float:
        """Evaluate board based on complexity and uniqueness."""
        solver = QueensSolver(board)
        solver.solve(6)
        num_solutions = solver.num_solutions
        return num_solutions
