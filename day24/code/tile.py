from enum import Enum


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
