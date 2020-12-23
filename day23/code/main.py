import logging

logger = logging.getLogger(__name__)


def displace_left(the_list, positions):
    positions = positions % len(the_list)

    for i in range(positions):
        the_list = the_list[1:] + [the_list[0]]

    return the_list


def displace_right(the_list, positions):
    positions = positions % len(the_list)

    for i in range(positions):
        the_list = [the_list[-1]] + the_list[:-1]

    return the_list


def play_cups_game(inp, max_moves=100, use_extended_rules=False):
    cups = [int(x) for x in inp.strip()]
    current_move = 1
    current_cup_index = 0

    if use_extended_rules:
        cups = cups + list(range(max(cups) + 1, max(cups) + 1 + 1000000 - len(cups)))

    while current_move <= max_moves:
        logger.info(f"-- move {current_move} --")
        logger.info(f"current cup index: {current_cup_index}")
        logger.info(
            f"cups: {' '.join([str(c) if i != current_cup_index else '(' + str(c) + ')' for i, c in enumerate(cups)])}")

        current_cup_label = cups[current_cup_index]

        # The crab picks up the three cups that are immediately clockwise of the current cup. They are removed from
        # the circle; cup spacing is adjusted as necessary to maintain the circle.

        pick_up_indices = [(current_cup_index + i) % len(cups) for i in range(1, 4)]
        picked_up = [cups[x] for x in pick_up_indices]

        for picked in picked_up:
            cups.remove(picked)

        logger.info(f"pick up: {', '.join(str(x) for x in picked_up)}")
        logger.info(
            f"after pickup: {' '.join([str(c) if i != current_cup_index else '(' + str(c) + ')' for i, c in enumerate(cups)])}")

        # The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. If
        # this would select one of the cups that was just picked up, the crab will keep subtracting one until it
        # finds a cup that wasn't just picked up. If at any point in this process the value goes below the lowest
        # value on any cup's label, it wraps around to the highest value on any cup's label instead.

        destination = current_cup_label - 1
        while True:
            if destination in cups:
                break

            elif destination in picked_up:
                destination -= 1

            if destination == 0:
                destination = max(cups)

        destination_index = cups.index(destination)
        logger.info(f"destination: {destination}")
        # logger.info(f"dest. index: {destination_index}")

        # The crab places the cups it just picked up so that they are immediately clockwise of the destination cup.
        # They keep the same order as when they were picked up.

        cups = cups[0:destination_index + 1] + picked_up + cups[destination_index + 1:]
        logger.info(
            f"after insert: {' '.join([str(c) if i != current_cup_index else '(' + str(c) + ')' for i, c in enumerate(cups)])}")

        # Displace the list so that the current cup stays at the same index
        displacement = cups.index(current_cup_label) - current_cup_index

        if displacement > 0:
            cups = displace_left(cups, displacement)
        else:
            cups = displace_right(cups, displacement)

        # # If the destination is left of the current cup, modify the cups list so that the current index stays correct
        # if destination_index < current_cup_index:
        #     old_cups = cups[:]
        #     cups = displace_left(cups, 3)
        #     logger.info(f"Displacing left:")
        #     logger.info(f"from {old_cups}")
        #     logger.info(f"to   {cups}")
        #
        # # If elements were picked from the left side of the current cup index, displace right
        # cups = displace_right(cups, picked_up_from_the_left)

        logger.info(
            f"after displace: {' '.join([str(c) if i != current_cup_index else '(' + str(c) + ')' for i, c in enumerate(cups)])}")

        # The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
        current_cup_index = (current_cup_index + 1) % len(cups)

        logger.info("")
        current_move += 1

    logger.info(f"Cups: {cups}")

    one_at = cups.index(1)
    return ''.join(str(x) for x in (cups[one_at + 1:] + cups[0:one_at]))
