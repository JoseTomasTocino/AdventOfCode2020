import logging
import os.path

from day14.code.main import sum_memory_values, sum_memory_values_v2

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""


def test_sample_input(caplog):
    # caplog.set_level(logging.INFO)
    assert sum_memory_values(sample_input) == 165


def test_sample_input_v2(caplog):
    # caplog.set_level(logging.INFO)

    inp = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""

    assert sum_memory_values_v2(inp) == 208


def test_big_input(caplog):
    # caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()
        assert sum_memory_values(content) == 8566770985168
        assert sum_memory_values_v2(content) == 4832039794082
