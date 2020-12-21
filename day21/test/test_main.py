import logging
import os.path

from day21.code.main import count_ingredients_without_allergens

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """trh fvjkl sbzzf mxmxvkd (contains dairy)
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""


def test_sample_input(caplog):
    caplog.set_level(logging.INFO)
    assert count_ingredients_without_allergens(sample_input) == 5


def test_big_input(caplog):
    caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert count_ingredients_without_allergens(content) == 2282
