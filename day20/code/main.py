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

    def get_variations(self):
        variations = []

        tile_t = deepcopy(self)
        tile_t.id = self.id + "_t"
        tile_t.transpose()
        variations.append(tile_t)

        for i in range(3):
            tile_r = deepcopy(self)
            tile_r.rotate(i + 1)
            tile_r.id = f"{self.id}_{90 * (i + 1)}"

            tile_rt = deepcopy(tile_t)
            tile_rt.rotate(i + 1)
            tile_rt.id = f"{tile_t.id}_{90 * (i + 1)}"

            variations.append(tile_r)
            variations.append(tile_rt)

        return variations


def generate_arrangement(tileset, width, so_far=None, depth=0):
    # Init container
    if so_far is None:
        so_far = []

    # Cache arrangement length
    len_so_far = len(so_far)

    # If arrangement is complete, return it
    if len_so_far == width * width:
        return so_far

    row = len_so_far // width
    col = len_so_far % width

    # Initially, the entire tileset is potentially usable
    potential_tiles = tileset

    # If not at topmost row, filter by valid bottom neighbors
    if row > 0:
        top_neighbor = so_far[(row - 1) * width + col]
        potential_tiles = [x for x in potential_tiles if not x.similar_to(top_neighbor) and x.bottom_of(top_neighbor)]

    # If not at leftmost col, filter by valid right neighbors
    if col > 0:
        left_neighbor = so_far[len_so_far - 1]
        potential_tiles = [x for x in potential_tiles if not x.similar_to(left_neighbor) and x.right_of(left_neighbor)]

    if not potential_tiles:
        return None

    # Recurse with each potential tile
    for potential in potential_tiles:
        res = generate_arrangement(tileset, width, so_far + [potential], depth=depth + 1)
        if res:
            return res


def rearrange_tiles(inp):
    tiles_raw = inp.split("\n\n")
    tileset = []

    # Parse input and generate initial tileset
    for tile_raw in tiles_raw:
        tile_raw = tile_raw.split("\n")

        id = re.search(r'\d+', tile_raw[0]).group(0)
        content = [list(x) for x in tile_raw[1:] if x]

        tile = Tile(id=id, content=content)
        tileset.append(tile)

    # Useful variables throughout
    original_tile_count = len(tileset)
    width = int(math.sqrt(original_tile_count))

    # Add rotations and flips of each tile
    for tile in tileset[:]:
        tileset += tile.get_variations()

    # Find the correct arrrangement
    arrangement = generate_arrangement(tileset, width)

    return arrangement


def multiply_corners(arrangement):
    width = int(math.sqrt(len(arrangement)))

    return arrangement[0] * arrangement[width - 1] * arrangement[width * width - width] * arrangement[width * width - 1]


def analyze_water_roughness(tileset):
    # Calculate some useful variables
    width = int(math.sqrt(len(tileset)))
    tile_width = len(tileset[0].content[0])

    # Make sure to remove the borders of each tile
    image_lines = []
    for i in range(0, width * width, width):
        for j in range(1, tile_width - 1):
            image_lines.append(list(''.join(''.join(t.content[j][1:-1]) for t in tileset[i:i + width])))

    # Use the Tile class to easily generate the variations
    image_tile = Tile(id='Image', content=image_lines)
    images = [image_tile] + image_tile.get_variations()

    monster = [
        '                  #',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #']

    # Convert monster lines to regexp by replace spaces with dots
    monster = [x.replace(' ', '.') for x in monster]

    # Try each variation of the image
    for image in images:
        image_lines = [''.join(x) for x in image.content]

        matches = []

        # Find middle line, then check lines above and below
        for i, image_line in enumerate(image_lines):

            # Ignore first and last lines
            if i == 0 or i == len(image_lines) - 1:
                continue

            # Match monster's middle line
            for match in re.finditer(monster[1], image_line):
                # Check line above
                prev_line_chunk = image_lines[i - 1][match.start():]
                if not re.match("^" + monster[0], prev_line_chunk):
                    continue

                # Check line below
                next_line_chunk = image_lines[i + 1][match.start():]
                if not re.match("^" + monster[2], next_line_chunk):
                    continue

                matches.append(i - 1)

        if matches:
            # Count total hashes, subtract hashes from matched sea monsters
            total_hashes = ''.join(image_lines).count('#')
            monster_hashes = ''.join(monster).count('#')

            return total_hashes - len(matches) * monster_hashes
