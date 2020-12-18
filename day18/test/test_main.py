import logging
import os.path

from day18.code.main import evaluate_expression

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = None


def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    assert evaluate_expression("1 + 2 * 3 + 4 * 5 + 6") == 71
    assert evaluate_expression("1 + (2 * 3) + (4 * (5 + 6))") == 51
    assert evaluate_expression("2 * 3 + (4 * 5)") == 26
    assert evaluate_expression("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
    assert evaluate_expression("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
    assert evaluate_expression("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632


def test_sample_input_with_advanced_priorities(caplog):
    caplog.set_level(logging.INFO)

    assert evaluate_expression("1 + 2 * 3 + 4 * 5 + 6", use_advanced_precedence=True) == 231
    assert evaluate_expression("1 + (2 * 3) + (4 * (5 + 6))", use_advanced_precedence=True) == 51
    assert evaluate_expression("2 * 3 + (4 * 5)", use_advanced_precedence=True) == 46
    assert evaluate_expression("5 + (8 * 3 + 9 + 3 * 4 * 3)", use_advanced_precedence=True) == 1445
    assert evaluate_expression("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", use_advanced_precedence=True) == 669060
    assert evaluate_expression("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", use_advanced_precedence=True) == 23340


def test_big_input(caplog):
    # caplog.set_level(logging.INFO)

    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()
        assert sum(evaluate_expression(x) for x in content.split("\n") if x) == 4696493914530
        assert sum(evaluate_expression(x, use_advanced_precedence=True) for x in content.split("\n") if x) == 362880372308125
