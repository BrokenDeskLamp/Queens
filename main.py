from board import Board
from placement import generate_queen_positions

# from scorer import Scorer
from colour import ColourSpread


def main(n):
    """Generate, fill, and evaluate an N x N board."""
    boards = []
    for i in range(100):
        board = Board(n)
        queen_positions = generate_queen_positions(n)
        board.place_queens(queen_positions)
        board.spread_colours(ColourSpread.random_spread)

        # score = Scorer.evaluate_board(board)
        score = 1
        boards.append((board, score))

    sorted_boards = sorted(boards, key=lambda x: x[1])
    best_board, best_score = sorted_boards[0]
    print(f"Best board score: {best_score}")
    print(best_board.grid)


if __name__ == "__main__":
    main(8)
