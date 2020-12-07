import logging
import re
import sys
from dataclasses import dataclass
from pprint import pprint, pformat

logger = logging.getLogger(__name__)
pp = lambda x: logger.info(pformat(x))


@dataclass
class BagNode:
    name: str
    capacity: map
    parents: set


def clean_bag_name(bag_name):
    match = re.match(r'(\d*)\s*([a-z ]+?)\s*bags?', bag_name.strip())

    if not match:
        return 0, None

    bag_type = match.group(2)
    bag_count = 1 if not match.group(1) else int(match.group(1))

    if bag_type.startswith("no other"):
        bag_type = None
        bag_count = 0

    return bag_count, bag_type


def count_shiny_gold_bag_parents(in_str):
    bag_nodes = {}

    rule_definitions = in_str.split(".\n")

    for rule in rule_definitions:
        rule_subject, rule_raw_content = rule.split(" contain ")

        # Parse rule_subject
        _, rule_subject = clean_bag_name(rule_subject)

        # Parse rule content
        rule_content = [clean_bag_name(x) for x in rule_raw_content.split(",")]
        bag_capacity = {x[1]: x[0] for x in rule_content}

        bag_nodes[rule_subject] = BagNode(name=rule_subject, capacity=bag_capacity, parents=set())

    # Compute parents
    for bag_type in bag_nodes:
        for bag_possible_parent in bag_nodes:
            if bag_type in bag_nodes[bag_possible_parent].capacity:
                bag_nodes[bag_type].parents.add(bag_possible_parent)

    # pp(bag_nodes)

    # Count shiny gold parents
    current_node = bag_nodes['shiny gold']

    found_parents = set()
    potential_nodes = set()
    revised_nodes = set()

    while True:
        # logger.info(f"{current_node=}")
        # pp(found_parents)
        # pp(potential_nodes)

        revised_nodes.add(current_node.name)

        for node in current_node.parents:
            if node not in revised_nodes:
                potential_nodes.add(node)

            if node not in found_parents:
                found_parents.add(node)

        if not potential_nodes:
            break

        current_node = bag_nodes[potential_nodes.pop()]

    return len(found_parents)
