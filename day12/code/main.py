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

    for action, value in instructions:
        logger.debug(f"Action = {action}, value = {value}, current position = {position}, orientation = {orientation}")

        if action == 'N':
            position[1] += value

        elif action == 'S':
            position[1] -= value

        elif action == 'E':
            position[0] += value

        elif action == 'W':
            position[0] -= value

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

    for action, value in instructions:
        logger.debug(f"Action = {action}, value = {value}, position = {position}, waypoint = {waypoint}")

        if action == 'N':
            waypoint[1] += value

        elif action == 'S':
            waypoint[1] -= value

        elif action == 'E':
            waypoint[0] += value

        elif action == 'W':
            waypoint[0] -= value

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
