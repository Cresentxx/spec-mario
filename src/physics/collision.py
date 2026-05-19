import pygame
from src.core.constants import TILE_SIZE, SOLID_TILES


def _float_overlap_x(body, tx):
    tile_left = tx * TILE_SIZE
    tile_right = tile_left + TILE_SIZE
    return body.x + body.width > tile_left and body.x < tile_right


def _float_overlap_y(body, ty):
    tile_top = ty * TILE_SIZE
    tile_bottom = tile_top + TILE_SIZE
    return body.y + body.height > tile_top and body.y < tile_bottom


def resolve_collisions_x(body, tile_map):
    top_tile = max(0, int(body.y) // TILE_SIZE)
    bot_tile = min(tile_map.height - 1, int(body.y + body.height) // TILE_SIZE)
    left_tile = max(0, int(body.x) // TILE_SIZE)
    right_tile = min(tile_map.width - 1, int(body.x + body.width) // TILE_SIZE)

    for ty in range(top_tile, bot_tile + 1):
        for tx in range(left_tile, right_tile + 1):
            if tile_map.get_tile(tx, ty) in SOLID_TILES:
                tile_left = tx * TILE_SIZE
                tile_right = tile_left + TILE_SIZE
                tile_top = ty * TILE_SIZE
                tile_bottom = tile_top + TILE_SIZE

                if (body.x + body.width > tile_left and body.x < tile_right and
                        body.y + body.height > tile_top and body.y < tile_bottom):
                    if body.vx > 0:
                        body.x = tile_left - body.width
                    elif body.vx < 0:
                        body.x = tile_right
                    body.vx = 0
                    return


def resolve_collisions_y(body, tile_map, hit_block_callback=None):
    body.on_ground = False
    top_tile = max(0, int(body.y) // TILE_SIZE)
    bot_tile = min(tile_map.height - 1, int(body.y + body.height) // TILE_SIZE)
    left_tile = max(0, int(body.x) // TILE_SIZE)
    right_tile = min(tile_map.width - 1, int(body.x + body.width) // TILE_SIZE)

    for ty in range(top_tile, bot_tile + 1):
        for tx in range(left_tile, right_tile + 1):
            if tile_map.get_tile(tx, ty) in SOLID_TILES:
                tile_left = tx * TILE_SIZE
                tile_right = tile_left + TILE_SIZE
                tile_top = ty * TILE_SIZE
                tile_bottom = tile_top + TILE_SIZE

                if (body.x + body.width > tile_left and body.x < tile_right and
                        body.y + body.height > tile_top and body.y < tile_bottom):
                    if body.vy >= 0:
                        body.y = tile_top - body.height
                        body.vy = 0
                        body.on_ground = True
                    elif body.vy < 0:
                        body.y = tile_bottom
                        body.vy = 0
                        if hit_block_callback:
                            hit_block_callback(tx, ty)
