import logging
import re

logger = logging.getLogger(__name__)


def decode_seat(seat):
    if not re.match(r"[FB]{7}[LR]{3}", seat):
        logger.error(f"Invalid seat code: {seat}")
        return -1

    # The seat string can be converted to binary and parsed, and that's it! lol
    return int(re.sub(r"[FL]", "0", re.sub(r"[BR]", "1", seat)), 2)


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
