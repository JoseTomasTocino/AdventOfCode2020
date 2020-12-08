import logging
import os.path

from day8.code.main import verify_boot_code, fix_boot_code

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""


def test_sample_input():
    assert verify_boot_code(sample_input) == (5, True)
    assert fix_boot_code(sample_input) == 8


def test_big_input():
    with open(os.path.join(local_path, "input"), 'r') as f:
        content = f.read()
        assert verify_boot_code(content) == (1867, True)
        assert fix_boot_code(content) == 1303
