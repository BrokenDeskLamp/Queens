from game import QueensGame
from solver import Solver
from model import GenerativeBoardGenerator
from objective import objective_function


def main():
    board_size = 8
    num_regions = 8
    game = QueensGame(board_size)

    # Generate a random board.
    random_board = game.generate_random_board()
    print("Randomly generated board:")
    random_board.display()

    # Solve the board.
    solver = Solver(game)
    num_solutions = solver.solve(random_board, max_count=2)
    print(f"Number of solutions: {num_solutions}")

    # Train the generative model.
    gen_model = GenerativeBoardGenerator(board_size, num_regions)
    gen_model.train(objective_function, num_epochs=5000)

    # Generate and display a board from the trained model.
    generated_board = gen_model.generate_board()
    print("Generated board:")
    generated_board.display()


if __name__ == "__main__":
    main()
