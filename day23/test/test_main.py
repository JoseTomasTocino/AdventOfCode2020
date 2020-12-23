import logging
import os.path

from day23.code.main import play_cups_game

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = None


# def test_displacement(caplog):
#     caplog.set_level(logging.INFO)
#
#     assert displace_left([1, 2, 3, 4, 5, 6], 2) == [3, 4, 5, 6, 1, 2]
#     assert displace_left([1, 2, 3, 4, 5, 6], 2 * 10) == [3, 4, 5, 6, 1, 2]
#
#     assert displace_right([1, 2, 3, 4, 5, 6], 2) == [5, 6, 1, 2, 3, 4]
#     assert displace_right([1, 2, 3, 4, 5, 6], 2 * 10) == [5, 6, 1, 2, 3, 4]


def test_sample_input(caplog):
    # caplog.set_level(logging.INFO)

    assert play_cups_game("389125467", max_moves=10) == "92658374"
    assert play_cups_game("389125467") == "67384529"

    # assert play_cups_game("389125467", use_extended_rules=True, max_moves=10000000) == "HOLA"


def test_big_input(caplog):
    # caplog.set_level(logging.INFO)

    assert play_cups_game("974618352") == "75893264"
