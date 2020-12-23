import logging
import os.path

from day05.code.main import decode_seat, check_boarding_pass_list, find_my_seat

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = None


def test_sample_input():
    assert decode_seat("FBFBBFFRLR") == 357
    assert decode_seat("BFFFBBFRRR") == 567
    assert decode_seat("FFFBBBFRRR") == 119
    assert decode_seat("BBFFBBFRLL") == 820


def test_big_input():
    with open(os.path.join(local_path, "input"), "r") as f:
        highest_bp_id = max(check_boarding_pass_list(f.read()))
        assert highest_bp_id == 976


def test_find_my_seat():
    with open(os.path.join(local_path, "input"), "r") as f:
        my_seat = find_my_seat(f.read())
        assert my_seat == 685
