import logging
import os.path

from day23.code.main import play_cups_game

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = None


def test_sample_input(caplog):
    # caplog.set_level(logging.INFO)

    assert play_cups_game("389125467", max_moves=10) == "92658374"
    assert play_cups_game("389125467") == "67384529"

    assert play_cups_game("389125467", use_extended_rules=True, max_moves=10000000) == 149245887792


def test_big_input(caplog):
    # caplog.set_level(logging.INFO)

    assert play_cups_game("974618352") == "75893264"
    assert play_cups_game("974618352", use_extended_rules=True, max_moves=10000000) == 38162588308
