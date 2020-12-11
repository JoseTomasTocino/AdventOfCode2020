import copy
import logging

logger = logging.getLogger(__name__)


def seat_matrix_to_string(seats):
    return "\n".join(["".join(x) for x in seats])


def get_adjacent_seats(seats, row, col, only_immediately_adjacent=True):
    row_count = len(seats)
    col_count = len(seats[0])

    adjacent_seats = []

    def find_next_seat_in_direction(dr, dc, delta_r, delta_c):
        while True:
            dr += delta_r
            dc += delta_c
            if not (0 <= dc < col_count and 0 <= dr < row_count):
                break

            if seats[dr][dc] != ".":
                return seats[dr][dc]

            if only_immediately_adjacent:
                break

        return None

    # Top
    adjacent_seats.append(find_next_seat_in_direction(row, col, 0, -1))
    # Bottom
    adjacent_seats.append(find_next_seat_in_direction(row, col, 0, +1))
    # Left
    adjacent_seats.append(find_next_seat_in_direction(row, col, -1, 0))
    # Right
    adjacent_seats.append(find_next_seat_in_direction(row, col, +1, 0))

    # DiagTopLeft
    adjacent_seats.append(find_next_seat_in_direction(row, col, -1, -1))
    # DiagBottomLeft
    adjacent_seats.append(find_next_seat_in_direction(row, col, +1, -1))
    # DiagTopRight
    adjacent_seats.append(find_next_seat_in_direction(row, col, -1, +1))
    # DiagBottomRight
    adjacent_seats.append(find_next_seat_in_direction(row, col, +1, +1))

    return adjacent_seats


def get_stable_occupied_seats(inp, extended_criteria=False):
    seats = [list(x) for x in inp.split("\n")]
    row_count = len(seats)
    col_count = len(seats[0])

    logger.debug(f"Row count: {row_count}, col count: {col_count}")
    logger.debug(f"Seats: \n{seat_matrix_to_string(seats)}")

    while True:
        updated_seats = copy.deepcopy(seats)

        for row in range(row_count):
            for col in range(col_count):
                if seats[row][col] == ".":
                    continue

                adjacent_seats = get_adjacent_seats(
                    seats, row, col, not extended_criteria
                )

                count_occupied_seats = sum(x == "#" for x in adjacent_seats)

                logger.debug(f"Current row={row}, col={col}, val={seats[row][col]}")
                logger.debug(f"Adjacent seats: {adjacent_seats}")
                logger.debug(f"Count occupied seats: {count_occupied_seats}")

                if seats[row][col] == "L" and count_occupied_seats == 0:
                    logger.debug("Seat becomes occupied")
                    updated_seats[row][col] = "#"

                elif seats[row][col] == "#" and count_occupied_seats >= (
                    5 if extended_criteria else 4
                ):
                    logger.debug("Seat becomes empty")
                    updated_seats[row][col] = "L"

        logger.debug("\n" + seat_matrix_to_string(updated_seats))

        if seat_matrix_to_string(updated_seats) == seat_matrix_to_string(seats):
            break

        seats = updated_seats

    return seat_matrix_to_string(seats).count("#")
