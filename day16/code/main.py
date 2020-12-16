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


def process_tickets_and_rules(inp):
    rules_section, own_ticket_section, other_tickets_section = inp.split("\n\n")

    # Parse rules
    rules = {}
    for match in re.finditer(r"([a-zA-Z ]+): (\d+)-(\d+) or (\d+)-(\d+)", rules_section):
        rules[match.group(1)] = ((int(match.group(2)), int(match.group(3))), (int(match.group(4)), int(match.group(5))))

    logger.info(f"Parsed rules:")
    for rname, rdef in rules.items():
        logger.info(f"    {rname}: {rdef}")

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

    # Check what rules match the nth field of each ticket
    num_fields = len(my_ticket)
    rules_for_nth_field = [[] for _ in range(num_fields)]

    for n in range(num_fields):
        for ticket in remaining_tickets:
            rules_for_nth_field[n].append(get_matching_rules(ticket[n], rules))

    # Isolate the rules that are matched by the nth field of all tickets
    final_rules = []
    for n in range(num_fields):
        final_rules.append((n, set.intersection(*[set(x) for x in rules_for_nth_field[n]])))

    # Sort by number of matching rules per field
    final_rules = sorted(final_rules, key=lambda x: len(x[1]))

    # Pretty print the rules:
    for n, rules in final_rules:
        logger.info(f"Field number {n} matches these rules: {rules}")

    logger.info("")
    logger.info("-------------")
    logger.info("")

    # Make the final rule assignment
    assigned_rules = recursively_check_rules([x[1] for x in final_rules])
    logger.info(f"Final: {assigned_rules}")

    # Multiply the values of my tickets for the fields that start with "departure"
    fields_product = 1
    for i, rr in enumerate(assigned_rules):
        if rr.startswith("departure"):
            j = final_rules[i][0]
            fields_product *= my_ticket[j]

    return sum(invalid_fields), fields_product


def recursively_check_rules(rules, depth=0):
    logger.info("")
    current_field_possible_rules = rules[0]

    logger.info(f"[DEPTH={depth}] Possible rules for current field: {current_field_possible_rules}")
    for possible_rule in current_field_possible_rules:
        modified_rules = deepcopy(rules)
        del modified_rules[0]

        for rule_set in modified_rules:
            if possible_rule in rule_set:
                rule_set.remove(possible_rule)

        logger.info(f"[DEPTH={depth}] Considering rule: {possible_rule}")
        logger.info(f"[DEPTH={depth}] Modified rules: (len={len(modified_rules)})")
        for ruleset in modified_rules:
            logger.info(f"[DEPTH={depth}]   {ruleset}")

        # If the union of all remaining rules is lower than the number of remaining fields, it's a dead end
        if len(modified_rules) < len(set.union(*[set(x) for x in modified_rules])):
            logger.info(
                f"[DEPTH={depth}] ### DEAD END, there are still {len(modified_rules)} fields but only {len(set.union(*[set(x) for x in modified_rules]))} rules to apply")
            continue

        if any(not x for x in modified_rules):
            logger.info(f"[DEPTH={depth}] ### DEAD END, there are fields with no applicable rules: {modified_rules}")
            continue

        if len(modified_rules) == 1 and len(modified_rules[0]) == 1:
            logger.info(f"[DEPTH={depth}] Reached base case, returning {modified_rules[0]}")
            return [possible_rule] + list(modified_rules[0])

        res = recursively_check_rules(modified_rules, depth=depth + 1)

        if res is not None:
            return [possible_rule] + res

        logger.info(f"[DEPTH={depth}] No luck for rule {possible_rule}")

    logger.info(f"[DEPTH={depth}] Oops, returning None")
    return None
