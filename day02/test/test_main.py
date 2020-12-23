import logging
import os.path

from day02.code.main import check_password_list, check_password_list_with_new_policy

logger = logging.getLogger(__name__)

local_path = os.path.abspath(os.path.dirname(__file__))


def test_sample_input():
    sample_input = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""

    assert check_password_list(sample_input) == 2


def test_big_input():
    with open(os.path.join(local_path, "input"), "r") as f:
        correct_passwords = check_password_list(f.read())
        logger.info(f"Correct passwords: {correct_passwords}")
        assert correct_passwords == 603


def test_sample_input_with_new_policy():
    sample_input = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""

    assert check_password_list_with_new_policy(sample_input) == 1


def test_big_input_with_new_policy():
    with open(os.path.join(local_path, "input"), "r") as f:
        correct_passwords = check_password_list_with_new_policy(f.read())
        logger.info(f"Correct passwords: {correct_passwords}")
        assert correct_passwords == 404
