import logging
import os.path

from day24.code.main import parse_directions_string, Direction, follow_directions, count_black_tiles

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""


def test_parse_directions(caplog):
    assert parse_directions_string('esenee') == [Direction.East, Direction.SouthEast, Direction.NorthEast,
                                                 Direction.East]


def test_follow_directions(caplog):
    assert follow_directions(parse_directions_string('esenee')) == (3, -3, 0)


def test_sample_input(caplog):
    assert count_black_tiles(sample_input) == 10
    caplog.set_level(logging.INFO)
    assert count_black_tiles(sample_input, run_art_exhibit=True) == 2208


def test_big_input(caplog):
    caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()
        assert count_black_tiles(content) == 232
        assert count_black_tiles(content, run_art_exhibit=True) == 232
