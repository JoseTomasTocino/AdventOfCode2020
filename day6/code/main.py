import logging
import re

logger = logging.getLogger(__name__)


def count_questions_anyone(in_str):
    return sum([len(set(x.replace("\n", ""))) for x in in_str.split("\n\n")])


def count_questions_everyone(in_str):
    return sum([len(set.intersection(*[set(x) for x in group.split("\n")])) for group in in_str.split("\n\n")])
