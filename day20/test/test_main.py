import logging
import os.path

from day20.code.main import rearrange_tiles, Tile, multiply_corners, analyze_water_roughness

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = None


def test_tile(caplog):
    caplog.set_level(logging.INFO)

    id = "123"
    content = [list("123"), list("456"), list("789")]

    tile = Tile(id=id, content=content)
    # assert tile.get_edges() == [['1', '1', '1'], ['1', '2', '3'], ['3', '3', '3'], ['3', '2', '1']]

    # tile.rotate()
    # logger.info(tile)

    # tile.transpose()
    # logger.info(tile)

    t1 = Tile(id="1", content=[[1, 2], [3, 4]])
    t2 = Tile(id="2", content=[[2, 2], [4, 4]])

    assert t2.right_of(t1)
    assert not t1.right_of(t2)

    t2 = Tile(id="2", content=[[3, 4], [9, 9]])

    assert t2.bottom_of(t1)
    assert not t1.bottom_of(t2)

    t1 = Tile(id="123", content=[])
    t2 = Tile(id="123_t_90", content=[])
    t3 = Tile(id="456", content=[])

    assert t1.similar_to(t2)
    assert not t1.similar_to(t3)


def test_sample_input(caplog):
    with open(os.path.join(local_path, "small_input"), "r") as f:
        content = f.read()

        tile_set = rearrange_tiles(content)
        tile_set_prod = multiply_corners([int(x.base_id) for x in tile_set])

        assert tile_set_prod == 20899048083289

        caplog.set_level(logging.INFO)
        assert analyze_water_roughness(tile_set) == 273


def test_big_input(caplog):
    # caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        tile_set = rearrange_tiles(content)
        tile_set_prod = multiply_corners([int(x.base_id) for x in tile_set])

        assert tile_set_prod == 7901522557967

        # caplog.set_level(logging.INFO)
        assert analyze_water_roughness(tile_set) == 2476
