from board import Board
from placement import generate_queen_positions
from spreading import apply_spreading
from scorer import Scorer
from visualisation import display_board


def main(n):
    """Generate, fill, and evaluate an N x N board."""
    board = Board(n)
    queen_positions = generate_queen_positions(n)
    board.place_queens(queen_positions)
    apply_spreading(board, strategy="random")

    score = Scorer.evaluate_board(board)
    print(f"Board Score: {score}")
    display_board(board)


if __name__ == "__main__":
    main(8)
