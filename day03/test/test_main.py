import logging
import os.path

from day03.code.main import traverse_map, get_map_cell, traverse_map_multiple_slopes

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))


def test_get_map_cell():
    map_template = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

    assert get_map_cell(map_template.split("\n"), 1, 10) == "."
    assert get_map_cell(map_template.split("\n"), 1, 10 + 11) == "."


def test_sample_input():
    map_template = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

    logger.info(traverse_map(map_template))


def test_sample_input_custom_slope():
    map_template = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

    assert traverse_map(map_template, slope=[1, 1]) == 2
    assert traverse_map(map_template, slope=[1, 3]) == 7
    assert traverse_map(map_template, slope=[2, 1]) == 2


def test_big_input():
    with open(os.path.join(local_path, "input"), "r") as f:
        found_trees = traverse_map(f.read())
        assert found_trees == 237


def test_sample_input_with_multiple_slopes():
    map_template = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

    tree_product = traverse_map_multiple_slopes(
        map_template, [[1, 1], [1, 3], [1, 5], [1, 7], [2, 1]]
    )
    assert tree_product == 336


def test_big_input_with_multiple_slopes():
    with open(os.path.join(local_path, "input"), "r") as f:
        tree_product = traverse_map_multiple_slopes(
            f.read(), [[1, 1], [1, 3], [1, 5], [1, 7], [2, 1]]
        )
        assert tree_product == 2106818610
