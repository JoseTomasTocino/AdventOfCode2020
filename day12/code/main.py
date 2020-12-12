import logging
import math

logger = logging.getLogger(__name__)


def parse_instructions(inp):
    return [(x[0], int(x[1:])) for x in inp.split("\n")]


def normalize_angle(angle):
    return (angle % 360 + 360) % 360


def get_ship_distance_from_start(inp):
    instructions = parse_instructions(inp)
    position = [0, 0]
    orientation = 0  # East

    # First value of the tuple is the coordinate to modify, second value is the factor to multiply by
    basic_actions = {'N': (1, 1), 'S': (1, -1), 'E': (0, 1), 'W': (0, -1)}

    for action, value in instructions:
        logger.debug(f"Action = {action}, value = {value}, current position = {position}, orientation = {orientation}")

        if action in basic_actions:
            position[basic_actions[action][0]] += value * basic_actions[action][1]

        elif action == 'L':
            orientation = normalize_angle(orientation + value)

        elif action == 'R':
            orientation = normalize_angle(orientation - value)

        elif action == 'F':
            position[0] += value * round(math.cos(orientation * math.pi / 180))
            position[1] += value * round(math.sin(orientation * math.pi / 180))

    logger.debug(f"Final position: {position}, final orientation: {orientation}")
    return abs(position[0]) + abs(position[1])


def get_ship_distance_with_waypoint(inp):
    instructions = parse_instructions(inp)
    position = [0, 0]
    waypoint = [10, 1]

    basic_actions = {'N': (1, 1), 'S': (1, -1), 'E': (0, 1), 'W': (0, -1)}

    for action, value in instructions:
        logger.debug(f"Action = {action}, value = {value}, position = {position}, waypoint = {waypoint}")

        if action in basic_actions:
            waypoint[basic_actions[action][0]] += value * basic_actions[action][1]

        elif action == 'R':
            value = normalize_angle(value)

            if value == 90:
                waypoint = [waypoint[1], -waypoint[0]]
            elif value == 180:
                waypoint = [-waypoint[0], -waypoint[1]]
            elif value == 270:
                waypoint = [-waypoint[1], waypoint[0]]

        elif action == 'L':
            value = normalize_angle(value)

            if value == 270:
                waypoint = [waypoint[1], -waypoint[0]]
            elif value == 180:
                waypoint = [-waypoint[0], -waypoint[1]]
            elif value == 90:
                waypoint = [-waypoint[1], waypoint[0]]

        elif action == 'F':
            position[0] += value * waypoint[0]
            position[1] += value * waypoint[1]

    logger.debug(f"Final position: {position}")
    return abs(position[0]) + abs(position[1])
