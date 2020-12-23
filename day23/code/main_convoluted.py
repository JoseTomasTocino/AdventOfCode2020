import dataclasses
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


# def displace_left(the_list, positions):
#     positions = positions % len(the_list)
#
#     for i in range(positions):
#         the_list = the_list[1:] + [the_list[0]]
#
#     return the_list
#
#
# def displace_right(the_list, positions):
#     positions = positions % len(the_list)
#
#     for i in range(positions):
#         the_list = [the_list[-1]] + the_list[:-1]
#
#     return the_list


@dataclass
class Node:
    first: int
    last: int
    next: 'Node' = dataclasses.field(default=None, repr=False)

    def is_single(self):
        return self.first == self.last

    def as_short_string(self):
        if self.is_single():
            return str(self.first)

        else:
            return f'{self.first}-{self.last}'

    def as_long_string(self):
        if self.is_single():
            return str(self.first)

        else:
            return ', '.join(str(x) for x in range(self.first, self.last + 1))

    def get(self, amount=3):
        the_next = []
        curr = self

        while len(the_next) < amount:
            curr.split()
            the_next.append(curr)
            curr = curr.next

        return the_next

    def get_next(self, amount=3):
        if not self.is_single():
            self.split()

        return self.next.get(amount=amount)

    def split(self):
        if self.is_single():
            return

        right = Node(first=self.first + 1, last=self.last, next=self.next)
        self.last = self.first
        self.next = right

        return self, right

    def chain_str(self, initial=None, expand=False):
        if initial == self:
            return ''

        else:
            if initial is None:
                initial = self

            s = self.as_long_string() if expand else self.as_short_string()

            if self.next is not None and self.next is not initial:
                s = s + ', ' + self.next.chain_str(initial=initial, expand=expand)

            return s

    def find(self, value):
        cur = self

        while True:
            if cur.first <= value <= cur.last:
                return cur

            cur = cur.next


def nodes_from_list(cups):
    i = 0
    nodes = []
    last_node = None

    # Create the nodes, using a single node for consecutive cups
    while i < len(cups):
        if last_node is None:
            last_node = Node(first=cups[i], last=cups[i])
            nodes.append(last_node)

        else:
            if cups[i] == cups[i - 1] + 1:
                last_node.last += 1

            else:
                last_node = Node(first=cups[i], last=cups[i])
                nodes[-1].next = last_node
                nodes.append(last_node)

        i += 1

    # Full circle!
    nodes[-1].next = nodes[0]

    return nodes


def play_cups_game(inp, max_moves=100, use_extended_rules=False):
    cups = [int(x) for x in inp.strip()]
    max_cup = max(cups)

    logger.info(f"Cups: {cups}")

    nodes = nodes_from_list(cups)

    current = nodes[0]
    current_move = 1

    if use_extended_rules:
        rest_node = Node(first=max_cup + 1, last=max_cup + 1000000 - len(cups), next=nodes[0])
        nodes[-1].next = rest_node
        max_cup = 1000000

    while current_move <= max_moves:
        if current_move % 1000 == 0:
            logger.error(current_move)

        logger.info(f"-- move {current_move} --")
        # logger.info(f"Nodes: {nodes[0].chain_str()}")

        # The crab picks up the three cups that are immediately clockwise of the current cup.
        picked_up = current.get_next(amount=3)
        picked_up_values = [x.first for x in picked_up]

        logger.info(f"pick up: {picked_up_values}")

        # They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.
        current.next = picked_up[-1].next
        picked_up[-1].next = None

        # The crab selects a destination cup: the cup with a label equal to the current cup's label minus one.
        destination = current.first - 1

        # If this would select one of the cups that was just picked up, the crab will keep subtracting one until it
        # finds a cup that wasn't just picked up. If at any point in this process the value goes below the lowest
        # value on any cup's label, it wraps around to the highest value on any cup's label instead.

        while True:
            if destination == 0:
                destination = max_cup

            if destination not in picked_up_values:
                break

            destination -= 1

        logger.info(f"destination: {destination}")
        destination = current.find(destination)

        # The crab places the cups it just picked up so that they are immediately clockwise of the destination cup.
        # They keep the same order as when they were picked up.

        picked_up[-1].next = destination.next
        destination.next = picked_up[0]

        # The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
        current = current.next

        logger.info("")
        current_move += 1

    node_one = nodes[0].find(1)
    if use_extended_rules:
        star_nodes = node_one.get_next(amount=2)
        retval = star_nodes[0].first * star_nodes[1].first

    else:
        retval = ''.join(node_one.chain_str(expand=True)[3:].split(", "))

    return retval
