import logging
from copy import deepcopy
from enum import Enum
from .tile import TileColor, Direction

from day24.code.interface import render_tileset

logger = logging.getLogger(__name__)


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


def neighbors(tile):
    x, y, z = tile
    deltas = [(1, 0, -1), (1, -1, 0), (0, -1, 1), (-1, 0, 1), (-1, 1, 0), (0, 1, -1)]

    return [(x + dx, y + dy, z + dz) for dx, dy, dz in deltas]


def step_tileset(tiles, modified_tiles=None):
    # Add surrounding border neighbors to modified tiles
    if modified_tiles is None:
        modified_tiles = list(tiles.keys())

    for tile in modified_tiles:
        for neighbor in neighbors(tile):
            if neighbor not in tiles:
                tiles[neighbor] = TileColor.White

    ntiles = deepcopy(tiles)

    # Every day, the tiles are all flipped according to the following rules:
    # - Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
    # - Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.

    modified_tiles = set()

    for tile, tile_color in tiles.items():
        count_black_neighbors = 0

        for neighbor in neighbors(tile):
            if neighbor in tiles and tiles[neighbor] == TileColor.Black:
                count_black_neighbors += 1

        if tile_color == TileColor.Black and (count_black_neighbors == 0 or count_black_neighbors > 2):
            ntiles[tile] = TileColor.White
            modified_tiles.add(tile)

        elif tile_color == TileColor.White and count_black_neighbors == 2:
            ntiles[tile] = TileColor.Black
            modified_tiles.add(tile)

    return ntiles, modified_tiles


def count_black_tiles(inp, run_art_exhibit=False):
    tiles = {}

    for case in inp.split("\n"):
        directions = parse_directions_string(case)
        final_position = follow_directions(directions)

        if final_position in tiles:
            tiles[final_position] = TileColor.Black if tiles[final_position] == TileColor.White else TileColor.White
        else:
            tiles[final_position] = TileColor.Black

    if run_art_exhibit:
        modified_tiles = None
        for i in range(100):
            tiles, modified_tiles = step_tileset(tiles, modified_tiles)

            # render_tileset(tiles)

    return sum(x.value for x in tiles.values())
