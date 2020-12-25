import logging
import os.path

from day25.code.main import transform_subject, reverse_loop_size, obtain_encryption_key

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = None


def test_transform(caplog):
    assert transform_subject(subject=17807724, loop_size=8) == 14897079
    assert transform_subject(subject=7, loop_size=11) == 17807724


def test_reverse_loop_size(caplog):
    assert reverse_loop_size(subject=7, result=5764801) == 8
    assert reverse_loop_size(subject=7, result=17807724) == 11


def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    assert obtain_encryption_key(5764801, 17807724) == 14897079


def test_big_input(caplog):
    caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        card_pk, door_pk = [int(x) for x in content.split("\n")]
        assert obtain_encryption_key(card_pk, door_pk) == 12227206
