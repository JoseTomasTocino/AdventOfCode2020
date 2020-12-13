import logging
import operator
import re
from functools import reduce
from math import ceil

logger = logging.getLogger(__name__)


def get_earliest_bus(inp):
    earliest_depart, bus_definitions = inp.split("\n")

    earliest_depart = int(earliest_depart)
    bus_definitions = [int(x) for x in bus_definitions.split(",") if re.match(r'^\d+$', x)]

    logger.debug(f"Earliest depart: {earliest_depart}, buses: {bus_definitions}")

    bus_nearest_arrivals = {bus * ceil(earliest_depart / bus): bus for bus in bus_definitions}

    logger.debug(f"Nearest arrivals: {bus_nearest_arrivals}")

    chosen_bus_next_depart = min(bus_nearest_arrivals.keys())
    chosen_bus = bus_nearest_arrivals[chosen_bus_next_depart]

    return earliest_depart, chosen_bus, chosen_bus_next_depart


def inverse_mod(a, b):
    """ Taken from https://shainer.github.io/crypto/math/2017/10/22/chinese-remainder-theorem.html """
    d = b
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return x0 % d


def chinese_remainder(pairs):
    """ Taken from https://shainer.github.io/crypto/math/2017/10/22/chinese-remainder-theorem.html """
    result = 0

    global_product = reduce(operator.mul, [x[0] for x in pairs], 1)

    for i in range(len(pairs)):
        ai = pairs[i][1]
        ni = pairs[i][0]
        bi = global_product // ni

        result += ai * bi * inverse_mod(bi, ni)

    return result % global_product


def get_earliest_timestamp_with_subsequent_departures(inp):
    bus_definitions = []
    for i, x in enumerate(inp.split("\n")[1].split(",")):
        if x == 'x':
            continue
        bus_definitions.append([int(x), int(x) - i])

    logger.debug(bus_definitions)

    return chinese_remainder(bus_definitions)
