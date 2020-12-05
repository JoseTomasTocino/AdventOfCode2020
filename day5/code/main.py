import logging
import re

logger = logging.getLogger(__name__)


def decode_seat(seat):
    if not re.match(r"[FB]{7}[LR]{3}", seat):
        logger.error(f"Invalid seat code: {seat}")
        return -1

    rows_interval = [0, 127]

    for i in range(7):
        interval_half_width = (rows_interval[1] - rows_interval[0] + 1) // 2

        if seat[i] == 'F':
            rows_interval[1] -= interval_half_width

        elif seat[i] == 'B':
            rows_interval[0] += interval_half_width

    cols_interval = [0, 7]

    for i in range(7, 7 + 3):
        interval_half_width = (cols_interval[1] - cols_interval[0] + 1) // 2

        if seat[i] == 'L':
            cols_interval[1] -= interval_half_width

        elif seat[i] == 'R':
            cols_interval[0] += interval_half_width

    return rows_interval[0] * 8 + cols_interval[0]


def check_boarding_pass_list(bp_list):
    return [decode_seat(seat) for seat in bp_list.split('\n') if seat.strip()]


def find_my_seat(bp_list):
    seat_list = set(check_boarding_pass_list(bp_list))

    min_seat_list = min(seat_list)
    max_seat_list = max(seat_list)

    correct_seat_list = set(range(min_seat_list, max_seat_list + 1))

    missing_seats = correct_seat_list.difference(seat_list)
    for missing_seat in missing_seats:
        if missing_seat not in [min_seat_list, max_seat_list]:
            return missing_seat

    return -1
