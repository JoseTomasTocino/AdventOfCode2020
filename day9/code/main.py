import logging

logger = logging.getLogger(__name__)


def find_bad_number(inp, preamble_size):
    numbers = [int(x) for x in inp.split("\n")]
    number_count = len(numbers)

    preamble_start = 0
    preamble_end = preamble_size - 1

    while preamble_end + 1 < number_count:
        target_number = numbers[preamble_end + 1]

        # Find operands in preamble
        found_operands = False

        for i in range(preamble_start, preamble_end + 1):
            for j in range(i + 1, preamble_end + 1):
                if numbers[i] + numbers[j] == target_number:
                    found_operands = True
                    break

            if found_operands:
                break

        if not found_operands:
            return target_number

        preamble_start += 1
        preamble_end += 1


def find_contiguous_sum_set(inp, target_number):
    numbers = [int(x) for x in inp.split("\n")]
    number_count = len(numbers)

    for i in range(number_count):
        set_size = 2

        # Keep increasing the window size until the size limit is reached or the sum equals the target number
        while i + set_size < number_count:
            if sum(numbers[i : i + set_size - 1]) == target_number:
                return numbers[i : i + set_size - 1]

            set_size += 1

    return None
