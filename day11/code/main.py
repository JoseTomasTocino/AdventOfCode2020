import copy
import logging

logger = logging.getLogger(__name__)


def seat_matrix_to_string(seats):
    return "\n".join(["".join(x) for x in seats])


def get_adjacent_seats(seats, row, col, only_immediately_adjacent=True):
    row_count = len(seats)
    col_count = len(seats[0])

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

    axis = [(0, -1), (0, +1), (-1, 0), (+1, 0), (-1, -1), (+1, -1), (-1, +1), (+1, +1)]
    adjacent_seats = [find_next_seat_in_direction(row, col, x, y) for x, y in axis]

    return adjacent_seats


def get_stable_occupied_seats(inp, extended_criteria=False):
    seats = [list(x) for x in inp.split("\n")]
    row_count = len(seats)
    col_count = len(seats[0])

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

                if seats[row][col] == "L" and count_occupied_seats == 0:
                    updated_seats[row][col] = "#"

                elif seats[row][col] == "#" and count_occupied_seats >= (
                        5 if extended_criteria else 4
                ):
                    updated_seats[row][col] = "L"

        if seat_matrix_to_string(updated_seats) == seat_matrix_to_string(seats):
            break

        seats = updated_seats

    return seat_matrix_to_string(seats).count("#")
