import logging
import os.path

from day11.code.main import get_stable_occupied_seats

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""


def test_sample_input(caplog):
    assert get_stable_occupied_seats(sample_input) == 37
    assert get_stable_occupied_seats(sample_input, extended_criteria=True) == 26


def test_big_input():
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert get_stable_occupied_seats(content) == 2299
        assert get_stable_occupied_seats(content, extended_criteria=True) == 2047
