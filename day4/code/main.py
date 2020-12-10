import logging
import re

logger = logging.getLogger(__name__)


def validate_field(field, value):
    if field == "byr":
        if not re.match(r"^\d{4}$", value) or int(value) < 1920 or int(value) > 2002:
            return False

    elif field == "iyr":
        if not re.match(r"^\d{4}$", value) or int(value) < 2010 or int(value) > 2020:
            return False

    elif field == "eyr":
        if not re.match(r"^\d{4}$", value) or int(value) < 2020 or int(value) > 2030:
            return False

    elif field == "hgt":
        match = re.match(r"^(\d+)(cm|in)$", value)

        if not match:
            return False

        elif match.group(2) == "cm" and (
            int(match.group(1)) < 150 or int(match.group(1)) > 193
        ):
            return False

        elif match.group(2) == "in" and (
            int(match.group(1)) < 59 or int(match.group(1)) > 76
        ):
            return False

    elif field == "hcl":
        if not re.match(r"^#[0-9a-f]{6}$", value):
            return False

    elif field == "ecl":
        if value not in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}:
            return False

    elif field == "pid":
        if not re.match(r"^\d{9}$", value):
            return False

    return True


def validate_single_passport(passport, check_fields=False):
    required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    optional_fields = ["cid"]

    passport_components = {
        x.split(":")[0]: x.split(":")[1]
        for x in re.split(r"\s+", passport)
        if x.strip()
    }
    logger.info(f"Passport components: {passport_components}")

    if not set(passport_components.keys()).issuperset(required_fields):
        return False

    if check_fields:
        for field in required_fields:
            if not validate_field(field, passport_components[field]):
                return False

    return True


def validate_passports(instr, check_fields=False):
    passports = instr.split("\n\n")
    logger.info(f"Detected {len(passports)} passports")

    valid_passports = 0

    for passport in passports:
        if validate_single_passport(passport, check_fields=check_fields):
            valid_passports += 1

    return valid_passports
