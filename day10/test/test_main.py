import logging
import os.path

from day10.code.main import get_adapter_differences, get_adapter_path_count

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = None


def test_sample_input():
    inp = """16
10
15
5
1
11
7
19
6
12
4"""

    differences = get_adapter_differences(inp)
    assert (differences.count(3) * differences.count(1)) == 35

    assert get_adapter_path_count(inp) == 8


def test_sample_input_2():
    inp = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

    differences = get_adapter_differences(inp)
    assert (differences.count(3) * differences.count(1)) == 220

    assert get_adapter_path_count(inp) == 19208


def test_big_input():
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        differences = get_adapter_differences(content)
        logger.info(f"Part 1 solution: {differences.count(3) * differences.count(1)}")

        logger.info(f"Part 2 solution: {get_adapter_path_count(content)}")
