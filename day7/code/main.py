import logging
import re
from dataclasses import dataclass
from pprint import pprint, pformat

logger = logging.getLogger(__name__)
pp = lambda x: logger.info(pformat(x))


@dataclass
class BagNode:
    name: str
    capacity: map
    parents: set


def clean_bag_name(bag_name: str) -> tuple:
    """
    Parses a string with a bag description and returns a tuple with the components
    :param bag_name: a string describing a bag type
    :return: a tuple with two elements: the bag count (or 1 if not specified) and the bag name

    >>> clean_bag_name("dark red bags")
    (1, 'dark red')
    >>> clean_bag_name("2 dark violet bags")
    (2, 'dark violet')
    """

    if bag_name.startswith("no other"):
        return 0, None

    match = re.match(r"(\d*)\s*([a-z ]+?)\s*bags?", bag_name.strip())

    if not match:
        return 0, None

    bag_type = match.group(2)
    bag_count = 1 if not match.group(1) else int(match.group(1))

    return bag_count, bag_type


def parse_bag_rules(in_str):
    """
    Parses a string with bag composition rules, creating a tree of BagNode items
    """

    bag_nodes = {}

    rule_definitions = in_str.split(".\n")

    for rule in rule_definitions:
        rule_subject, rule_raw_content = rule.split(" contain ")

        # Parse rule_subject
        _, rule_subject = clean_bag_name(rule_subject)

        # Parse rule content
        rule_content = [clean_bag_name(x) for x in rule_raw_content.split(",")]
        bag_capacity = {x[1]: x[0] for x in rule_content}

        if None in bag_capacity:
            bag_capacity = {}

        bag_nodes[rule_subject] = BagNode(
            name=rule_subject, capacity=bag_capacity, parents=set()
        )

    # Compute parents
    for bag_type in bag_nodes:
        for bag_possible_parent in bag_nodes:
            if bag_type in bag_nodes[bag_possible_parent].capacity:
                bag_nodes[bag_type].parents.add(bag_possible_parent)

    return bag_nodes


def count_shiny_gold_bag_parents(in_str):
    """
    Counts the number of ancestors a shiny gold bag can have
    """

    bag_nodes = parse_bag_rules(in_str)

    current_node = bag_nodes["shiny gold"]

    found_parents = set()
    potential_nodes = set()
    revised_nodes = set()

    while True:
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


def count_bag_node_children(bag_nodes, bag_type):
    """
    Count how many bags a bag of type bag_type can hold
    """

    children_count = 0

    for child, child_count in bag_nodes[bag_type].capacity.items():
        children_count += child_count + child_count * count_bag_node_children(
            bag_nodes, child
        )

    return children_count


def count_shiny_gold_bag_children(in_str):
    """
    Counts how many bags a shiny gold bag holds
    """

    bag_nodes = parse_bag_rules(in_str)
    return count_bag_node_children(bag_nodes, "shiny gold")
