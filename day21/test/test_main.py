import logging
import os.path

from day21.code.main import count_ingredients_without_allergens, get_canonical_dangerous_ingredients

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """trh fvjkl sbzzf mxmxvkd (contains dairy)
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""


def test_sample_input(caplog):
    # caplog.set_level(logging.INFO)
    assert count_ingredients_without_allergens(sample_input) == 5
    assert get_canonical_dangerous_ingredients(sample_input) == 'mxmxvkd,sqjhc,fvjkl'


def test_big_input(caplog):
    # caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert count_ingredients_without_allergens(content) == 2282
        assert get_canonical_dangerous_ingredients(content) == 'vrzkz,zjsh,hphcb,mbdksj,vzzxl,ctmzsr,rkzqs,zmhnj'
