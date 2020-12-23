import logging
import os.path

from day4.code.main import validate_passports, validate_field

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

invalid_passports_input = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""

valid_passports_input = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""


def test_sample_input():
    assert validate_passports(sample_input) == 2


def test_big_input():
    with open(os.path.join(local_path, "input"), "r") as f:
        valid_passports = validate_passports(f.read())
        assert valid_passports == 233
        logger.info(f"Valid passports: {valid_passports}")


def test_validate_fields():
    assert validate_field("byr", "2002")
    assert validate_field("byr", "2003") is False

    assert validate_field("hgt", "60in")
    assert validate_field("hgt", "190cm")

    assert validate_field("hgt", "190in") is False
    assert validate_field("hgt", "190") is False

    assert validate_field("hcl", "#123abc")
    assert validate_field("hcl", "#123abz") is False
    assert validate_field("hcl", "123abc") is False

    assert validate_field("ecl", "brn")
    assert validate_field("ecl", "wat") is False

    assert validate_field("pid", "000000001")
    assert validate_field("pid", "0123456789") is False


def test_validate_passports_with_valid_fields():
    assert validate_passports(valid_passports_input, check_fields=True) == 4


def test_validate_passports_with_invalid_fields():
    assert validate_passports(invalid_passports_input, check_fields=True) == 0


def test_big_input_checking_fields():
    with open(os.path.join(local_path, "input"), "r") as f:
        valid_passports = validate_passports(f.read(), check_fields=True)
        assert valid_passports == 111
        logger.info(f"Valid passports: {valid_passports}")
