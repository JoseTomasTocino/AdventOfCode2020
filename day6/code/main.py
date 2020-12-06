import logging
import re

logger = logging.getLogger(__name__)


def count_questions(in_str):
    # Isolate groups
    yes_count = sum([len(set(x.replace("\n", ""))) for x in in_str.split("\n\n")])

    return yes_count
