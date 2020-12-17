import logging
import os.path

from day17.code.main import simulate_cycles

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = None


def test_sample_input(caplog):
    # caplog.set_level(logging.INFO)
    inp = """.#.
..#
###"""

    assert simulate_cycles(inp, 6) == 112
    assert simulate_cycles(inp, 6, dimensions=4) == 848


def test_big_input(caplog):
    # caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert simulate_cycles(content, 6) == 336
        assert simulate_cycles(content, 6, dimensions=4) == 2620
