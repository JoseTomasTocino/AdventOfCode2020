import logging

logger = logging.getLogger(__name__)


def play_cups_game(inp, max_moves=100, use_extended_rules=False):
    labels = [int(x) for x in inp]

    # Map where the key is the label, and the value is the next element
    next_map = {}
    for i in range(len(labels)):
        # The next of the last element is the first element
        if i == len(labels) - 1:
            next_map[labels[i]] = labels[0]

        else:
            next_map[labels[i]] = labels[i + 1]

    current = labels[0]
    max_cup = max(labels)

    # With extended rules, add the rest of the numbers up until 1 million in consecutive order
    if use_extended_rules:
        for i in range(max_cup + 1, 1000000):
            next_map[i] = i + 1

        next_map[1000000] = next_map[labels[-1]]
        next_map[labels[-1]] = max_cup + 1
        max_cup = 1000000

    for move in range(max_moves):
        # The crab picks up the three cups that are immediately clockwise of the current cup.
        next_1 = next_map[current]
        next_2 = next_map[next_1]
        next_3 = next_map[next_2]

        # They are removed from the circle
        next_map[current] = next_map[next_3]

        # The crab selects a destination cup: the cup with a label equal to the current cup's label minus one.
        destination = current - 1

        while True:
            # If at any point in this process the value goes below the lowest value on any cup's label,
            # it wraps around to the highest value on any cup's label instead.
            if destination == 0:
                destination = max_cup

            # If this would select one of the cups that was just picked up, the crab will keep subtracting one until it
            # finds a cup that wasn't just picked up.
            if destination not in [next_1, next_2, next_3]:
                break

            destination -= 1

        # The crab places the cups it just picked up so that they are immediately clockwise of the destination cup.
        next_map[next_3] = next_map[destination]
        next_map[destination] = next_1

        # The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
        current = next_map[current]

    if use_extended_rules:
        # The crab is going to hide your stars - one each - under the two cups that will end up immediately clockwise
        # of cup 1. What do you get if you multiply their labels together?

        retval = next_map[1] * next_map[next_map[1]]

    else:
        # Starting after the cup labeled 1, collect the other cups' labels clockwise into a single string with no extra
        # characters; each number except 1 should appear exactly once.

        labels_in_order = []
        n = next_map[1]
        while n != 1:
            labels_in_order.append(n)
            n = next_map[n]

        retval = ''.join(str(x) for x in labels_in_order)

    return retval
