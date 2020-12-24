import logging
from enum import Enum

logger = logging.getLogger(__name__)


class Direction(Enum):
    # Using this: https://www.redblobgames.com/grids/hexagons/#coordinates-cube
    NorthEast = (1, 0, -1)
    East = (1, -1, 0)
    SouthEast = (0, -1, 1)
    SouthWest = (-1, 0, 1)
    West = (-1, 1, 0)
    NorthWest = (0, 1, -1)


class TileColor(Enum):
    White = 0
    Black = 1


def parse_directions_string(s):
    dir_map = {
        'nw': Direction.NorthWest,
        'w': Direction.West,
        'sw': Direction.SouthWest,
        'se': Direction.SouthEast,
        'e': Direction.East,
        'ne': Direction.NorthEast
    }

    directions = []
    i = 0
    while i < len(s):
        # e, se, sw, w, nw, and ne
        if s[i] in ('e', 'w'):
            directions.append(dir_map[s[i]])
        else:
            i += 1
            directions.append(dir_map[s[i - 1] + s[i]])

        i += 1

    return directions


def follow_directions(directions, initial=(0, 0, 0)):
    for direction in directions:
        initial = (initial[0] + direction.value[0], initial[1] + direction.value[1], initial[2] + direction.value[2])

    return initial


def count_black_tiles(inp):
    tiles = {}
    for case in inp.split("\n"):
        directions = parse_directions_string(case)
        final_position = follow_directions(directions)

        if final_position in tiles:
            logger.info(f"Inverting color of tile {final_position}")
            tiles[final_position] = TileColor.Black if tiles[final_position] == TileColor.White else TileColor.White
        else:
            logger.info(f"Flipping tile {final_position}")
            tiles[final_position] = TileColor.Black

    return sum(x.value for x in tiles.values())
