import logging
import os.path

from day7.code.main import count_shiny_gold_bag_parents, clean_bag_name

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""


def test_clean_bag_name():
    assert clean_bag_name("light red bags") == (1, "light red")
    assert clean_bag_name("1 bright white bag") == (1, "bright white")
    assert clean_bag_name("2 muted yellow bags") == (2, "muted yellow")
    assert clean_bag_name("no other bags") == (0, None)


def test_sample_input():
    assert count_shiny_gold_bag_parents(sample_input) == 4


def test_big_input():
    with open(os.path.join(local_path, "input"), 'r') as f:
        assert count_shiny_gold_bag_parents(f.read()) == 259
