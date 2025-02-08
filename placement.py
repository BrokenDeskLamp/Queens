from random import shuffle


def generate_queen_positions(n):
    """Generate a valid N-Queens solution."""
    cols = list(range(n))
    shuffle(cols)
    return [(i, cols[i]) for i in range(n)]
