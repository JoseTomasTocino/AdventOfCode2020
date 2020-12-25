import math
import logging
from day24.code.tile import TileColor, Direction
import pygame
from pygame import gfxdraw

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


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


def render_tileset(tiles):
    win_size = (800, 800)
    center = (win_size[0] // 2, win_size[1] // 2)
    margin = 50

    converted_positions = [cube_to_offset(x) for x in tiles.keys()]

    min_col = min(x[0] for x in converted_positions)
    max_col = max(x[0] for x in converted_positions)
    col_span = max_col - min_col + 1

    logger.info(f"Min col: {min_col}, max col: {max_col}, col_span: {col_span}")

    min_row = min(x[1] for x in converted_positions)
    max_row = max(x[1] for x in converted_positions)
    row_span = max_row - min_row + 1

    logger.info(f"Min row: {min_row}, max row: {max_row}, row_span: {row_span}")

    span = max(col_span, row_span)

    radius = (win_size[0] - 2 * margin) / span / 2
    sepradius = 1.1 * radius
    inradius = math.sqrt(3) / 2 * sepradius

    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode(win_size)

    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        screen.fill((255, 255, 255))

        # Draw a solid blue circle in the center
        # pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

        for i, (tile_pos, tile_color) in enumerate(tiles.items()):
            tile_pos = list(cube_to_offset(tile_pos))
            # logger.info(f"Placing hexagon at {tile_pos}")
            tile_pos[0] = center[0] + (2 * inradius * tile_pos[0]) + tile_pos[1] % 2 * inradius
            tile_pos[1] = center[1] + (1.5 * sepradius) * tile_pos[1]

            tile_color = (0, 0, 0) if tile_color == TileColor.Black else (255, 255, 255)
            tile_stroke = (0, 0, 0) if tile_color != TileColor.Black else (255, 255, 255)
            draw_hexagon(screen, tile_pos, tile_color, radius, 0.1 * radius, tile_stroke)

            # if i == 2:
            #     break

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()


if __name__ == '__main__':
    tileset = {
        (0, 0, 0): TileColor.Black,
        (1, -1, 0): TileColor.White,
        (1, 0, -1): TileColor.Black,
        (0, 1, -1): TileColor.White,
        (-1, 1, 0): TileColor.Black,
        (-1, 0, 1): TileColor.White,
        (0, -1, 1): TileColor.Black
    }

    render_tileset(tileset)
