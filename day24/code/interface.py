import math
import logging
import os

from day24.code.main import count_black_tiles, step_tileset
from day24.code.tile import TileColor, Direction
import pygame
from pygame import gfxdraw

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

local_path = os.path.abspath(os.path.dirname(__file__))
test_path = os.path.join(local_path, '..', 'test')


def get_hexagon_coordinates(center, radius):
    coordinates = []

    v = pygame.Vector2()
    v.x = 0
    v.y = -radius

    for ang in range(6):
        coordinates.append((center[0] + v.x, center[1] + v.y))
        v.rotate_ip(360 // 6)

    return coordinates


def draw_hexagon(surface, center, color, radius, stroke_width=None, stroke_color=(0, 0, 0)):
    if stroke_width is not None:
        hex_coords = get_hexagon_coordinates(center, radius + stroke_width)
        pygame.gfxdraw.aapolygon(surface, hex_coords, stroke_color)
        pygame.gfxdraw.filled_polygon(surface, hex_coords, stroke_color)

    hex_coords = get_hexagon_coordinates(center, radius)
    pygame.gfxdraw.aapolygon(surface, hex_coords, color)
    pygame.gfxdraw.filled_polygon(surface, hex_coords, color)


def cube_to_offset(pos):
    x, y, z = pos
    col = x + (z - (z & 1)) / 2
    row = z

    return col, row


def render():
    win_size = (800, 800)
    center = (win_size[0] // 2, win_size[1] // 2)
    margin = 50

    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode(win_size)

    content = open(os.path.join(test_path, "input"), "r").read()

    tiles, _ = count_black_tiles(content)
    modified_tiles = None

    def recalculate_dimensions():
        converted_positions = [cube_to_offset(x) for x in tiles.keys()]

        min_col = min(x[0] for x in converted_positions)
        max_col = max(x[0] for x in converted_positions)
        col_span = max_col - min_col + 1

        min_row = min(x[1] for x in converted_positions)
        max_row = max(x[1] for x in converted_positions)
        row_span = max_row - min_row + 1

        span = max(col_span, row_span)

        radius = (win_size[0] - 2 * margin) / span / 2
        sepradius = 1.1 * radius
        inradius = math.sqrt(3) / 2 * sepradius

        return radius, sepradius, inradius

    radius, sepradius, inradius = recalculate_dimensions()

    pygame.time.set_timer(pygame.USEREVENT + 1, 200)

    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif (event.type == pygame.KEYUP and event.key == pygame.K_SPACE) or event.type == pygame.USEREVENT + 1:
                tiles, modified_tiles = step_tileset(tiles, modified_tiles)
                radius, sepradius, inradius = recalculate_dimensions()

        # Fill the background with white
        screen.fill((255, 255, 255))

        for i, (tile_pos, tile_color) in enumerate(tiles.items()):
            tile_pos = list(cube_to_offset(tile_pos))
            # logger.info(f"Placing hexagon at {tile_pos}")
            tile_pos[0] = center[0] + (2 * inradius * tile_pos[0]) + tile_pos[1] % 2 * inradius
            tile_pos[1] = center[1] + (1.5 * sepradius) * tile_pos[1]

            tile_color = (0, 0, 0) if tile_color == TileColor.Black else (255, 255, 255)
            tile_stroke = (0, 0, 0) if tile_color != TileColor.Black else (255, 255, 255)
            draw_hexagon(screen, tile_pos, tile_color, radius, 0.1 * radius, tile_stroke)

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()


if __name__ == '__main__':
    render()
