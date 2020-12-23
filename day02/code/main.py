import logging
import re

logger = logging.getLogger(__name__)


def get_policy_components(policy):
    policy_match = re.match(r"(\d+)-(\d+)\s+([a-zA-Z]+)", policy)

    leftr = int(policy_match.group(1))
    rightr = int(policy_match.group(2))
    char = policy_match.group(3).strip()

    return (leftr, rightr, char)


def check_password_list(l):
    correct_passwords = 0

    for policy, password in [x.split(": ") for x in l.split("\n")]:
        logger.info(f"Policy: {policy}, password: {password}")

        policy_min, policy_max, policy_char = get_policy_components(policy)

        password_char_count = password.count(policy_char)

        if policy_min <= password_char_count <= policy_max:
            correct_passwords += 1

    return correct_passwords


def check_password_list_with_new_policy(l):
    correct_passwords = 0

    for policy, password in [x.split(": ") for x in l.split("\n")]:
        logger.info(f"Policy: {policy}, password: '{password}'")

        first_position, second_position, policy_char = get_policy_components(policy)

        char_in_first = password[first_position - 1] == policy_char
        char_in_second = password[second_position - 1] == policy_char

        if char_in_first != char_in_second:
            correct_passwords += 1

    return correct_passwords
