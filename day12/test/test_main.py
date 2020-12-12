import logging
import os.path

from day12.code.main import parse_instructions, get_ship_distance_from_start, get_ship_distance_with_waypoint

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

inp = """F10
N3
F7
R90
F11"""


def test_parse_instructions():
    assert parse_instructions(inp) == [('F', 10), ('N', 3), ('F', 7), ('R', 90), ('F', 11)]


def test_sample_input(caplog):
    caplog.set_level(logging.DEBUG)

    assert get_ship_distance_from_start(inp) == 25
    assert get_ship_distance_with_waypoint(inp) == 286


def test_big_input(caplog):
    caplog.set_level(logging.INFO)

    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert get_ship_distance_from_start(content) == 2280
        assert get_ship_distance_with_waypoint(content) == 38693
