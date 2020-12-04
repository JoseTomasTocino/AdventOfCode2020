import logging
import os.path

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = None


def test_sample_input():
    pass


def test_big_input():
    with open(os.path.join(local_path, "input"), 'r') as f:
        f.read()
