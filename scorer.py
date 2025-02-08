import numpy as np


class Scorer:
    @staticmethod
    def evaluate_board(board):
        """Evaluate board based on complexity and uniqueness."""
        color_diversity = len(set(board.grid.flatten()))  # Number of unique colors
        filled_ratio = np.count_nonzero(board.grid) / (board.n**2)  # Percentage of board filled
        return color_diversity * filled_ratio  # Simple heuristic, can be improved
