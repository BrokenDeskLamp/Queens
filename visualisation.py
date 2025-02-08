import matplotlib.pyplot as plt


def display_board(board):
    """Display the board using matplotlib."""
    plt.imshow(board.grid, cmap="tab10")
    plt.colorbar()
    plt.show()
