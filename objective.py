from solver import Solver
from game import QueensGame


def objective_function(board) -> float:
    game = QueensGame(board.board_size)
    solver = Solver(game)
    solution_count = solver.solve(board, max_count=2)
    uniqueness_reward = 1.0 if solution_count == 1 else 1.0 / (solution_count + 1)
    difficulty_reward = game.evaluate_difficulty(board)
    alpha, beta = 10.0, 1.0
    total_reward = uniqueness_reward + beta * difficulty_reward - alpha * max(0, solution_count - 1)
    return total_reward
