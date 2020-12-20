import logging
import math
import re
from copy import deepcopy

logger = logging.getLogger(__name__)


class Tile:
    def __init__(self, id, content):
        self.id = id
        self.base_id = id.split("_")[0]
        self.content = content

    def get_edges(self):
        edges = list()

        # Top
        edges.append(self.content[0])

        # Right
        edges.append(list(x[-1] for x in self.content))

        # Bottom
        edges.append(self.content[-1])

        # Left
        edges.append([x[0] for x in self.content])

        return edges

    def flip_horizontally(self):
        self.content = [x[::-1] for x in self.content]

    def flip_vertically(self):
        self.content = self.content[::-1]

    def rotate(self, turns=1):
        for i in range(turns):
            dim = len(self.content[0])
            self.content = [[self.content[row][col] for row in range(dim - 1, -1, -1)] for col in range(dim)]

    def transpose(self):
        new_content = deepcopy(self.content)
        dim = len(self.content[0])

        for i in range(dim):
            for j in range(dim):
                self.content[i][j] = new_content[j][i]

    def __str__(self):
        return f"Tile: {self.id}\n" + '\n'.join(''.join(x) for x in self.content)

    def __repr__(self):
        return f"Tile: {self.id}"

    def adjacent_to(self, other_tile):
        if self.id == other_tile.id or self.id in other_tile.id or other_tile.id in self.id:
            return False

        my_edges = set(tuple(x) for x in self.get_edges())
        other_edges = set(tuple(x) for x in other_tile.get_edges())

        if my_edges.intersection(other_edges):
            return True

        return False

    def right_of(self, other):
        my_left = [x[0] for x in self.content]
        his_right = [x[-1] for x in other.content]

        return my_left == his_right

    def bottom_of(self, other):
        my_top = self.content[0]
        his_bottom = other.content[-1]

        return my_top == his_bottom

    def similar_to(self, other):
        return self.id.split("_")[0] == other.id.split("_")[0]


def generate_arrangement(tileset, width, so_far=None, depth=0):
    # Init container
    if so_far is None:
        so_far = []

    logger.info(f"[DEPTH={depth}] {'    ' * depth}Generating arrangements, {width=} so_far = {[x.id for x in so_far]}")

    # If arrangement is complete, return it (yield?)
    len_so_far = len(so_far)
    if len_so_far == width * width:
        logger.info(f"[DEPTH={depth}] {'    ' * depth}BASE CASE")
        return so_far

    row = len_so_far // width
    col = len_so_far % width

    logger.info(f"[DEPTH={depth}] {'    ' * depth}   Current {row=}, {col=}")

    potential_tiles = tileset

    # If not at topmost row, filter by valid bottom neighbors
    if row > 0:
        top_neighbor = so_far[(row - 1) * width + col]
        logger.info(f"[DEPTH={depth}] {'    ' * depth}   Has top neighbor: {top_neighbor.id}")
        potential_tiles = [x for x in potential_tiles if not x.similar_to(top_neighbor) and x.bottom_of(top_neighbor)]

    # If not at leftmost col, filter by valid right neighbors
    if col > 0:
        left_neighbor = so_far[len_so_far - 1]
        logger.info(f"[DEPTH={depth}] {'    ' * depth}   Has left neighbor: {left_neighbor.id}")
        potential_tiles = [x for x in potential_tiles if not x.similar_to(left_neighbor) and x.right_of(left_neighbor)]

    # # First cell, the entire tileset is possible
    # if row == 0 and col == 0:
    #     potential_tiles = tileset
    #
    # # If not at topmost row, add top neighbor
    # if row > 0:
    #     top_neighbor = so_far[len_so_far - 1 - width]
    #     logger.info(f"[DEPTH={depth}] {'    ' * depth}   Has top neighbor: {top_neighbor.id}")
    #     potential_tiles += [x for x in tileset if not x.similar_to(top_neighbor) and x.bottom_of(top_neighbor)]
    #
    # # If not at leftmost col, add left neighbor
    # if col > 0:
    #     left_neighbor = so_far[len_so_far - 1]
    #     logger.info(f"[DEPTH={depth}] {'    ' * depth}   Has left neighbor: {left_neighbor.id}")
    #     potential_tiles += [x for x in tileset if not x.similar_to(left_neighbor) and x.right_of(left_neighbor)]

    logger.info(
        f"[DEPTH={depth}] {'    ' * depth}   Found {len(potential_tiles)} potential tiles: {[x.id for x in potential_tiles]}")

    if not potential_tiles:
        return None

    for potential in potential_tiles:
        logger.info(f"[DEPTH={depth}] {'    ' * depth}   Trying potential: {potential.id}")
        # logger.info(potential)
        res = generate_arrangement(tileset, width, so_far + [potential], depth=depth + 1)
        if res:
            return res


def rearrange_tiles(inp):
    tiles_raw = inp.split("\n\n")
    corner_tiles = []
    tileset = []

    for tile_raw in tiles_raw:
        tile_raw = tile_raw.split("\n")
        id = re.search(r'\d+', tile_raw[0]).group(0)
        content = [list(x) for x in tile_raw[1:] if x]

        tile = Tile(id=id, content=content)
        tileset.append(tile)

    original_tile_count = len(tileset)
    width = int(math.sqrt(original_tile_count))
    tile_width = len(tileset[0].content[0])

    logger.info(f"Found {original_tile_count} tiles, matrix: {width}x{width}, tile width: {tile_width}")

    # Add rotations and flips
    for tile in tileset[:]:
        tile_t = deepcopy(tile)
        tile_t.id = tile.id + "_t"
        tile_t.transpose()
        tileset.append(tile_t)

        for i in range(3):
            tile_r = deepcopy(tile)
            tile_r.rotate(i + 1)
            tile_r.id = f"{tile.id}_{90 * (i + 1)}"

            tile_rt = deepcopy(tile_t)
            tile_rt.rotate(i + 1)
            tile_rt.id = f"{tile_t.id}_{90 * (i + 1)}"

            tileset.append(tile_r)
            tileset.append(tile_rt)

    comb = generate_arrangement(tileset, width)

    logger.info([x.id for x in comb])

    for i in range(0, width * width, width):
        for j in range(tile_width):
            logger.info(' '.join(''.join(t.content[j]) for t in comb[i:i + width]))
        logger.info("")

    return comb


def multiply_corners(arrangement):
    width = int(math.sqrt(len(arrangement)))

    return arrangement[0] * arrangement[width - 1] * arrangement[width * width - width] * arrangement[width * width - 1]
