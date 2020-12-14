import logging
import re

logger = logging.getLogger(__name__)


def sum_memory_values(inp):
    mask = None
    mem_values = {}

    for line in inp.split("\n"):
        if line.startswith("mask"):
            mask = line.split(" = ")[1]

            logger.info(f"Mask set to {mask}")

        elif line.startswith("mem"):
            match = re.match(r"^mem\[(\d+)\] = (\d+)$", line)
            write_position = int(match.group(1))
            write_value = bin(int(match.group(2)))[2:].zfill(len(mask))

            logger.info(f"Write at position {write_position}, value = {write_value}")

            if mask is None:
                continue

            actual_value = ''.join([mask[i] if mask[i] != 'X' else write_value[i] for i in range(len(mask))])
            logger.info(f"  Actual value:              {actual_value}")

            mem_values[write_position] = actual_value

    return sum(int(x, 2) for x in mem_values.values())


def sum_memory_values_v2(inp):
    mask = None
    mem_values = {}

    for line in inp.split("\n"):
        if line.startswith("mask"):
            mask = line.split(" = ")[1]

            logger.info(f"Mask set to {mask}")

        elif line.startswith("mem"):
            match = re.match(r"^mem\[(\d+)\] = (\d+)$", line)
            write_position = bin(int(match.group(1)))[2:].zfill(len(mask))
            write_value = int(match.group(2))

            logger.info(f"Write at position:     {write_position}, value = {write_value}")

            # Apply mask to write_position
            new_write_position = ''.join([write_position[i] if mask[i] == '0' else mask[i] for i in range(len(mask))])
            logger.info(f"Actual write position: {new_write_position}")

            floating_bit_indices = [m.start() for m in re.finditer('X', mask)]
            logger.info(f"Floating bits positions: {floating_bit_indices}")

            for i in range(2 ** len(floating_bit_indices)):
                replacement = bin(i)[2:].zfill(len(floating_bit_indices))
                logger.info(f"  Replacement: {replacement}")

                generated_position = list(new_write_position)

                for j in range(len(floating_bit_indices)):
                    logger.info(f"  Rewriting bit at position {floating_bit_indices[j]} with bit {replacement[j]}")
                    generated_position[floating_bit_indices[j]] = replacement[j]

                generated_position = ''.join(generated_position)
                logger.info(f"  Generated position: {generated_position} (decimal {int(generated_position, 2)})")

                mem_values[int(generated_position, 2)] = write_value

    return sum(mem_values.values())
