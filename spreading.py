from colour import ColorSpread


def apply_spreading(board, strategy="random"):
    """Apply a spreading strategy to the board."""
    strategies = {
        "random": ColorSpread.random_spread,
        # Future strategies can be added here
    }
    strategy_func = strategies.get(strategy, ColorSpread.random_spread)
    board.spread_colors(strategy_func)
