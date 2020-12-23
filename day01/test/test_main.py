import logging
import os

from day01.code.main import process_input, get_number_group

logger = logging.getLogger(__name__)

local_path = os.path.abspath(os.path.dirname(__file__))


def test_case_1():
    input_str = """1721
979
366
299
675
1456"""

    assert process_input(input_str) == 514579


def test_case_2():
    input_str = """1721
979
366
299
675
1456"""

    assert process_input(input_str, num_components=3) == 241861950


def test_input():
    with open(os.path.join(local_path, "input"), "r") as f:
        input_str = f.read()
        output = process_input(input_str)
        logger.info(f"Output: {output}")

        assert output == 388075


def test_input_with_three_components():
    with open(os.path.join(local_path, "input"), "r") as f:
        input_str = f.read()
        output = process_input(input_str, num_components=3)
        logger.info(f"Output: {output}")

        assert output == 293450526


def test_get_number_group():
    numbers_in = [1, 2, 3, 4]

    numbers_out = list(get_number_group(numbers_in, num_components=1))
    assert numbers_out == [[1], [2], [3], [4]]

    numbers_out = list(get_number_group(numbers_in, num_components=2))
    assert numbers_out == [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]

    numbers_out = list(get_number_group(numbers_in, num_components=3))
    assert numbers_out == [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]
