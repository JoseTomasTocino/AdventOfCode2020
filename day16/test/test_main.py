import logging
import os.path

from day16.code.main import get_ticket_error_rate, get_matching_rules

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))


def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    sample_input = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
    assert get_ticket_error_rate(sample_input) == 71


def test_part_2(caplog):
    caplog.set_level(logging.INFO)
    inp = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""

    assert get_ticket_error_rate(inp) == 71


def test_get_matching_rules(caplog):
    caplog.set_level(logging.INFO)

    rules = {'rule a': ((2, 5), (10, 15)), 'rule b': ((0, 1), (4, 8))}

    assert get_matching_rules(3, rules) == ['rule a']
    assert get_matching_rules(1, rules) == ['rule b']
    assert get_matching_rules(4, rules) == ['rule a', 'rule b']
    assert get_matching_rules(20, rules) == []


def test_big_input(caplog):
    caplog.set_level(logging.INFO)

    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()
        assert get_ticket_error_rate(content) == 19070
