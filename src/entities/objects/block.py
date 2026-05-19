import pygame
from src.core.constants import TILE_SIZE, TILE_QUESTION, TILE_BRICK, TILE_USED, TILE_AIR, FORM_SMALL, FORM_SUPER, FORM_FIRE


class BlockManager:
    def __init__(self, block_defs):
        self.blocks = {}
        for bd in block_defs:
            tx, ty = bd["x"], bd["y"]
            self.blocks[(tx, ty)] = {
                "type": bd["type"],
                "content": bd.get("content", "coin"),
                "bounce_timer": 0,
                "active": True,
            }

    def hit_block(self, tx, ty, player_form, tile_map):
        key = (tx, ty)
        info = self.blocks.get(key)
        tile_id = tile_map.get_tile(tx, ty)

        if tile_id == TILE_QUESTION:
            tile_map.set_tile(tx, ty, TILE_USED)
            if info:
                info["bounce_timer"] = 8
            content = info["content"] if info else "coin"
            return ("spawn", content, tx, ty)

        if tile_id == TILE_BRICK:
            if player_form in (FORM_SUPER, FORM_FIRE):
                tile_map.set_tile(tx, ty, TILE_AIR)
                return ("break", None, tx, ty)
            else:
                if info:
                    info["bounce_timer"] = 8
                return ("bounce", None, tx, ty)

        return None

    def update(self):
        for info in self.blocks.values():
            if info["bounce_timer"] > 0:
                info["bounce_timer"] -= 1

    def get_bounce_offset(self, tx, ty):
        info = self.blocks.get((tx, ty))
        if info and info["bounce_timer"] > 0:
            t = info["bounce_timer"]
            if t > 4:
                return -(t - 4) * 2
            else:
                return t * 2
        return 0
