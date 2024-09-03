"""Utility code for a simple simulated robot application.

Author: Nathan Sprague
Version: 8/25/2022
"""
from typing import Tuple

Location = Tuple[int, int]


def get_neighbor(loc: Location, direction: int) -> Location:
    """Get the neighboring location in the indicated direction.

    Args:
        loc: A tuple representing the x, y coordinates of a location.
        direction: An integer in the range 0-3, were 0 = North, 1 = East
            2 = South and 3 = West

    Returns:
        The coordinates of the appropriate neighbor location.
    """
    if direction == 0:
        next_loc = (loc[0], loc[1] + 1)
    elif direction == 1:
        next_loc = (loc[0] + 1, loc[1])
    elif direction == 2:
        next_loc = (loc[0], loc[1] - 1)
    elif direction == 3:
        next_loc = (loc[0] - 1, loc[1])
    elif direction is None:
        next_loc = loc
    else:
        raise ValueError(f"Invalid direction: {direction}")
    return next_loc
