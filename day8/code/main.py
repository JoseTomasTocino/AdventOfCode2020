import copy
import logging

logger = logging.getLogger(__name__)


def verify_boot_code(boot_code):
    """
    Verifies the input boot code, computing the accumulator value and checking if the program runs infinitely. If an
    infinite loop is detected, the execution is halted. The function returns a tuple where the first element is the
    value of the accumulator when the program is finished, and the second element is a boolean indicating whether the
    program runs infinitely or not.
    """

    instructions = [x.split(" ") for x in boot_code.split("\n")]
    instructions_count = len(instructions)

    executed_instructions = set()
    accumulator = 0
    current_instruction_index = 0
    is_infinite = False

    # Instruction loop
    while current_instruction_index < instructions_count:

        # If the current instruction was executed before, an infinite loop has been found, so stop processing
        if current_instruction_index in executed_instructions:
            is_infinite = True
            break

        executed_instructions.add(current_instruction_index)

        instruction_type, instruction_argument = instructions[current_instruction_index]

        if instruction_type == 'nop':
            current_instruction_index += 1

        elif instruction_type == 'acc':
            accumulator += int(instruction_argument)
            current_instruction_index += 1

        elif instruction_type == 'jmp':
            current_instruction_index += int(instruction_argument)

    return accumulator, is_infinite


def fix_boot_code(boot_code):
    """
    Fixes the given boot code, that runs infinitely, by morphing one 'nop' or 'jmp' at a time and running the program.
    It returns the value of the accumulator when the modified program is no longer infinite.
    """

    instructions = [x.split(" ") for x in boot_code.split("\n")]

    # Go over each instruction in the program
    for i, instruction in enumerate(instructions):

        # Don't modify 'acc' instructions
        if instruction[0] == 'acc':
            continue

        # Make a copy of the program, morphing the i-th instruction
        modified_instructions = copy.deepcopy(instructions)
        modified_instructions[i][0] = 'jmp' if modified_instructions[i][0] == 'nop' else 'nop'

        # Check if the modified program runs infinitely
        acc, is_infinite = verify_boot_code('\n'.join([' '.join(x) for x in modified_instructions]))

        if not is_infinite:
            return acc

    return None
