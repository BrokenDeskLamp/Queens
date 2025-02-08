import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def display_board(board):
    region_colors = {
        1: "#FFDDC1",  # Light Peach
        2: "#FFABAB",  # Light Red
        3: "#FFC3A0",  # Orange
        4: "#D5AAFF",  # Light Purple
        5: "#85E3FF",  # Light Blue
        6: "#B9FBC0",  # Light Green
        7: "#FFABE1",  # Pink
        8: "#FFFFB5",  # Yellow
    }
    """Display the board using matplotlib."""
    size = board.shape[0]
    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw the board regions
    for row in range(size):
        for col in range(size):
            region = int(board[row, col])
            color = region_colors.get(region, "white")
            ax.add_patch(Rectangle((col, size - row - 1), 1, 1, color=color))

    # Add the grid
    for x in range(size + 1):
        ax.axhline(x, color="black", linewidth=0.5)
        ax.axvline(x, color="black", linewidth=0.5)

    # Set limits and aspect
    ax.set_xlim(0, size)
    ax.set_ylim(0, size)
    ax.set_aspect("equal")
    ax.axis("off")

    plt.show()
