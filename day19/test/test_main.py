import logging
import os.path

from day19.code.main import count_valid_messages

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = None


def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    inp = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""

    assert count_valid_messages(inp) == 2


def test_medium_input(caplog):
    caplog.set_level(logging.INFO)

    with open(os.path.join(local_path, "medium_input"), "r") as f:
        content = f.read()

        assert count_valid_messages(content, consider_loopin_rules=False) == 3
        assert count_valid_messages(content, consider_loopin_rules=True) == 12


def test_big_input(caplog):
    caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert count_valid_messages(content, consider_loopin_rules=False) == 118
        assert count_valid_messages(content, consider_loopin_rules=True) == 246
