import functools
import logging
import operator

logger = logging.getLogger(__name__)


def get_number_group(numbers, num_components=1):
    for i, n in enumerate(numbers):
        if num_components == 1:
            yield [n]
        else:
            for subgroup in get_number_group(numbers[i + 1 :], num_components - 1):
                yield [n] + subgroup


def process_input(s, num_components=2):
    numbers = [int(x.strip()) for x in s.split("\n")]

    numbers.sort(reverse=True)

    for group in get_number_group(numbers, num_components):
        if sum(group) == 2020:
            return functools.reduce(operator.mul, group)
