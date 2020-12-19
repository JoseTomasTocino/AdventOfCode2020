import logging
import re
from dataclasses import dataclass
from enum import Enum

from pprint import pformat

logger = logging.getLogger(__name__)


class NodeType(Enum):
    Leaf = 1
    Branching = 2
    Ruleset = 3


@dataclass
class Node:
    node_type: NodeType
    value: str = None  # For leaf nodes
    lbranch: 'Node' = None  # For multioption nodes
    rbranch: 'Node' = None  # For multioption nodes
    ruleset: list = None  # For ruleset nodes

    def to_expr(self, rules_container):
        if self.node_type == NodeType.Leaf:
            return self.value

        elif self.node_type == NodeType.Branching:
            return f'({self.lbranch.to_expr(rules_container)}|{self.rbranch.to_expr(rules_container)})'

        elif self.node_type == NodeType.Ruleset:
            return ''.join(rules_container[rule].to_expr(rules_container) for rule in self.ruleset)


def count_valid_messages(inp, consider_loopin_rules=False):
    rules_raw, messages_raw = inp.split("\n\n")

    rules = {r.split(": ")[0]: r.split(": ")[1] for r in rules_raw.split("\n")}
    messages = messages_raw.split("\n")

    if consider_loopin_rules:
        rules['8'] = "42 | 42 8"
        rules['11'] = "42 31 | 42 11 31"

    logger.info(f"Rules: {rules}")
    logger.info(f"Messages: {messages}")

    final_rules = {}

    # Parse rule tree
    for rname, rdef in rules.items():
        logger.info(f"Parsing rule {rname}, definition: {rdef}")

        # Leaf node
        if '"' in rdef:
            value = rdef.strip('"')
            logger.info(f"  Leaf node, value: {value}")

            final_rules[rname] = Node(node_type=NodeType.Leaf, value=value)

        # Multioption node
        elif "|" in rdef:
            lbranch, rbranch = [x.split(" ") for x in rdef.split(" | ")]
            logger.info(f"  Branch node, left: {lbranch}, right: {rbranch}")

            lnode = Node(node_type=NodeType.Ruleset, ruleset=lbranch)
            rnode = Node(node_type=NodeType.Ruleset, ruleset=rbranch)

            final_rules[rname] = Node(node_type=NodeType.Branching, lbranch=lnode, rbranch=rnode)

        # Ruleset node
        else:
            ruleset = rdef.split(" ")
            logger.info(f"  Ruleset node: {ruleset}")

            final_rules[rname] = Node(node_type=NodeType.Ruleset, ruleset=ruleset)

    logger.info(pformat(final_rules))

    message_format = "^" + final_rules['0'].to_expr(rules_container=final_rules) + "$"
    logger.info(f"Message format: {message_format}")

    return sum(1 if re.match(message_format, x) else 0 for x in messages)
