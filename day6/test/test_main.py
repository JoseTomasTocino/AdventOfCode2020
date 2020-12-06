import logging
import os.path

from day6.code.main import count_questions

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """abc

a
b
c

ab
ac

a
a
a
a

b"""


def test_sample_input():
    assert count_questions(sample_input) == 11


def test_big_input():
    with open(os.path.join(local_path, "input"), 'r') as f:
        highest_bp_id = count_questions(f.read())
        assert highest_bp_id == 6387
#
#
# def test_find_my_seat():
#     with open(os.path.join(local_path, "input"), 'r') as f:
#         my_seat = find_my_seat(f.read())
#         assert my_seat == 685
