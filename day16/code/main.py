import logging
import re
from copy import deepcopy

logger = logging.getLogger(__name__)


def get_matching_rules(value, rules):
    matching_rules = []

    for rule, intervals in rules.items():
        if any(interval_start <= value <= interval_end for interval_start, interval_end in intervals):
            matching_rules.append(rule)

    return matching_rules


def get_ticket_error_rate(inp):
    rules_section, own_ticket_section, other_tickets_section = inp.split("\n\n")

    # Parse rules
    rules = {}
    for match in re.finditer(r"(\w+): (\d+)-(\d+) or (\d+)-(\d+)", rules_section):
        rules[match.group(1)] = ((int(match.group(2)), int(match.group(3))), (int(match.group(4)), int(match.group(5))))

    # Parse own ticket
    my_ticket = [int(x) for x in own_ticket_section.split("\n")[1].split(",")]

    # Parse other tickets
    other_tickets = [[int(x) for x in t.split(",")] for t in other_tickets_section.split("\n")[1:]]

    # Determine completely invalid tickets
    invalid_fields = []
    remaining_tickets = []

    for ticket in other_tickets:
        ticket_is_invalid = False

        for value in ticket:
            matching_rules = get_matching_rules(value, rules)

            if not matching_rules:
                invalid_fields.append(value)
                ticket_is_invalid = True

        if not ticket_is_invalid:
            remaining_tickets.append(ticket)

    # Compute the rules matching the nth field of each ticket
    num_fields = len(my_ticket)
    rules_for_nth_field = [[] for _ in range(num_fields)]

    for n in range(num_fields):
        for ticket in remaining_tickets:
            rules_for_nth_field[n].append(get_matching_rules(ticket[n], rules))

    # Isolate the rules that are matched by the nth field of all tickets
    for n in range(num_fields):
        rules_for_nth_field[n] = set.intersection(*[set(x) for x in rules_for_nth_field[n]])

    # Pretty print the rules:
    for n in range(num_fields):
        logger.info(f"Field number {n} matches these rules: {rules_for_nth_field[n]}")

    return 0
    # Make the final rule assignment
    logger.info(f"Final: {recursively_check_rules(rules_for_nth_field)}")

    return sum(invalid_fields)


def recursively_check_rules(rules):
    logger.info(f"Recursively checking rules: {rules}")

    current_field_possible_rules = rules[0]

    for possible_rule in current_field_possible_rules:
        modified_rules = deepcopy(rules)
        del modified_rules[0]

        for rule_set in modified_rules:
            if possible_rule in rule_set:
                rule_set.remove(possible_rule)

        logger.info(f"Considering rule: {possible_rule}, Modified rules: {modified_rules}")

        # If the union of all remaining rules is lower than the number of remaining fields, it's a dead end
        if len(modified_rules) < len(set.union(*[set(x) for x in modified_rules])):
            logger.info(
                f"### DEAD END, there are still {len(modified_rules)} fields but only {len(set.union(*[set(x) for x in modified_rules]))} rules to apply")
            continue

        if any(not x for x in modified_rules):
            logger.info(f"### DEAD END, there are fields with no applicable rules: {modified_rules}")
            continue

        if len(modified_rules) == 1 and len(modified_rules[0]) == 1:
            logger.info(f"Reached base case, returning {modified_rules[0]}")
            return [possible_rule] + list(modified_rules[0])

        res = recursively_check_rules(modified_rules)

        if res is not None:
            return [possible_rule] + res

    logger.info("Oops, returning None")
    return None
