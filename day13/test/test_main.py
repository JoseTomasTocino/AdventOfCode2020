import logging
import os.path

from day13.code.main import get_earliest_bus, get_earliest_timestamp_with_subsequent_departures

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = None


def test_sample_input(caplog):
    inp = """939
7,13,x,x,59,x,31,19"""

    earliest_depart, chosen_bus, chosen_bus_next_depart = get_earliest_bus(inp)
    assert (chosen_bus_next_depart - earliest_depart) * chosen_bus == 295

    assert get_earliest_timestamp_with_subsequent_departures(inp) == 1068781

    inp = """0
17,x,13,19"""
    assert get_earliest_timestamp_with_subsequent_departures(inp) == 3417

    inp = """0
67,7,59,61"""
    assert get_earliest_timestamp_with_subsequent_departures(inp) == 754018

    inp = """0
67,x,7,59,61"""
    assert get_earliest_timestamp_with_subsequent_departures(inp) == 779210

    inp = """0
67,7,x,59,61"""
    assert get_earliest_timestamp_with_subsequent_departures(inp) == 1261476

    inp = """0
1789,37,47,1889"""
    assert get_earliest_timestamp_with_subsequent_departures(inp) == 1202161486


def test_big_input(caplog):
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert get_earliest_timestamp_with_subsequent_departures(content) == 305068317272992
