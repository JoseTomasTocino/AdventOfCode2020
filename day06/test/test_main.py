import logging
import os.path

from day6.code.main import count_questions_anyone, count_questions_everyone

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
    assert count_questions_anyone(sample_input) == 11
    assert count_questions_everyone(sample_input) == 6


def test_big_input():
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()
        assert count_questions_anyone(content) == 6387
        assert count_questions_everyone(content) == 3039


#
#
# def test_find_my_seat():
#     with open(os.path.join(local_path, "input"), 'r') as f:
#         my_seat = find_my_seat(f.read())
#         assert my_seat == 685
