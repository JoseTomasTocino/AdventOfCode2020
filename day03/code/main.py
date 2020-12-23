import functools
import logging
import operator

logger = logging.getLogger(__name__)


def get_map_cell(map_template, row, column):
    column = column % len(map_template[0])
    return map_template[row][column]


def traverse_map(map_string, slope=[1, 3]):
    map_template = map_string.split("\n")
    num_rows = len(map_template)

    current_position = [0, 0]
    num_trees = 0

    while current_position[0] < num_rows:
        cell_type = get_map_cell(map_template, *current_position)

        if cell_type == "#":
            num_trees += 1

        current_position[0] += slope[0]
        current_position[1] += slope[1]

    return num_trees


def traverse_map_multiple_slopes(map_string, slopes):
    found_trees = []

    for slope in slopes:
        trees = traverse_map(map_string, slope)
        logger.info(f"Traversing with slope: {slope}, found trees: {trees}")
        found_trees.append(trees)

    return functools.reduce(operator.mul, found_trees)
