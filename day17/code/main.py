import logging
from copy import deepcopy
from enum import Enum
from itertools import combinations_with_replacement, permutations

logger = logging.getLogger(__name__)


class CubeState(Enum):
    Inactive = 0
    Active = 1


def cube_at(pos, pool):
    if pos in pool:
        return pool[pos]
    else:
        return CubeState.Inactive


def print_cubes(cubes):
    min_z = min(x[2] for x in cubes.keys())
    max_z = max(x[2] for x in cubes.keys())

    for z in range(min_z, max_z + 1):
        min_y = min(x[1] for x in cubes.keys() if x[2] == z)
        max_y = max(x[1] for x in cubes.keys() if x[2] == z)

        logger.info("")
        logger.info(f"z={z}")
        for y in range(min_y, max_y + 1):
            min_x = min(x[0] for x in cubes.keys() if x[1] == y and x[2] == z)
            max_x = max(x[0] for x in cubes.keys() if x[1] == y and x[2] == z)

            row = []

            for x in range(min_x, max_x + 1):
                row.append('#' if cube_at((x, y, z), cubes) == CubeState.Active else '.')

            logger.info(''.join(row))


def simulate_cycles(inp, cycles, dimensions=3):
    cubes = {}

    # Parse input
    for rnum, r in enumerate(inp.split("\n")):
        for cnum, c in enumerate(r):
            pos = tuple([cnum, rnum] + [0 for _ in range(dimensions - 2)])

            if c == '#':
                cubes[pos] = CubeState.Active
            else:
                cubes[pos] = CubeState.Inactive

    # Generate deltas
    deltas = set()
    for x in combinations_with_replacement([-1, 0, 1], dimensions):
        if x == (0,) * dimensions:
            continue

        deltas.update(set(permutations(x)))

    logger.info(f"Deltas (len={len(deltas)}): {deltas}")

    logger.info("Initial position:")
    print_cubes(cubes)

    logger.info("")
    logger.info("Starting simulation:")

    # Simulate cycles
    current_cycle = 1

    while current_cycle <= cycles:
        logger.info(f"Cycle number {current_cycle}")

        # Make a copy of the cube setup
        new_cubes = deepcopy(cubes)

        processed_positions = set()
        unprocessed_positions = set(new_cubes.keys())

        logger.info(f"{len(unprocessed_positions)} cubes to process initially")

        # Add neighbors
        new_neighbors = set()
        for cube_pos in unprocessed_positions:
            new_neighbors.update(set(tuple(cube_pos[c] + d[c] for c in range(dimensions)) for d in deltas))

        unprocessed_positions.update(new_neighbors)

        logger.info(f"{len(unprocessed_positions)} cubes to process (after adding neighbors)")

        for cube_pos in sorted(unprocessed_positions, key=lambda pp: (pp[2] * 10e5 + pp[1] * 10e3 + pp[0])):
            if cube_pos in processed_positions:
                continue

            processed_positions.add(cube_pos)

            cube = cube_at(cube_pos, cubes)

            neighbors_positions = set(tuple(cube_pos[c] + d[c] for c in range(dimensions)) for d in deltas)
            neighbors = [cube_at(neighbor_pos, cubes) for neighbor_pos in neighbors_positions]
            num_active_neighbors = sum(x == CubeState.Active for x in neighbors)

            logger.info(f"Cube at {cube_pos} is {'ACTIVE' if cube == CubeState.Active else 'INACTIVE'} and has {num_active_neighbors} active neighbors")

            if cube == CubeState.Active and num_active_neighbors not in [2, 3]:
                logger.info(f"    Changed to inactive")
                new_cubes[cube_pos] = CubeState.Inactive

            elif cube == CubeState.Inactive and num_active_neighbors == 3:
                logger.info(f"    Changed to active")
                new_cubes[cube_pos] = CubeState.Active

        # Print the current state
        logger.info("")
        logger.info(f"After {current_cycle} cycle")

        # print_cubes(new_cubes)

        current_cycle += 1

        cubes = new_cubes

    return sum(1 for x in cubes.values() if x == CubeState.Active)

