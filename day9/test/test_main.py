from day9.code.main import find_bad_number, find_contiguous_sum_set

import logging
import os.path

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = None


def test_sample_input():
    inp1 = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""
    preamble_size = 5

    assert find_bad_number(inp1, preamble_size) == 127
    assert find_contiguous_sum_set(inp1, 127) == [15, 25, 47, 40]


def test_sample_input_2():
    inp1 = """1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
49
100
50"""
    preamble_size = 25

    assert find_bad_number(inp1, preamble_size) == 100    


def test_big_input():
    with open(os.path.join(local_path, "input"), 'r') as f:
        content = f.read()
        assert find_bad_number(content, 25) == 1038347917

        components = find_contiguous_sum_set(content, 1038347917)
        assert min(components) + max(components) == 137394018
