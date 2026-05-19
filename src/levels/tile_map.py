import pygame
from src.core.constants import TILE_SIZE, TILE_AIR, TILE_HARD, TILE_BRICK, TILE_QUESTION, TILE_USED, TILE_HIDDEN, TILE_LAVA, BLACK, HARD_GRAY, BRICK_ORANGE, QUESTION_YELLOW, USED_BROWN, LAVA_RED


class TileMap:
    def __init__(self, tiles, width, height):
        self.tiles = tiles
        self.width = width
        self.height = height

    def get_tile(self, tx, ty):
        if 0 <= tx < self.width and 0 <= ty < self.height:
            return self.tiles[ty][tx]
        return TILE_AIR

    def set_tile(self, tx, ty, tile_id):
        if 0 <= tx < self.width and 0 <= ty < self.height:
            self.tiles[ty][tx] = tile_id

    @property
    def pixel_width(self):
        return self.width * TILE_SIZE

    def draw(self, surface, camera_x):
        start_col = max(0, camera_x // TILE_SIZE)
        end_col = min(self.width, (camera_x + surface.get_width()) // TILE_SIZE + 2)

        for ty in range(self.height):
            for tx in range(start_col, end_col):
                tile_id = self.tiles[ty][tx]
                if tile_id == TILE_AIR:
                    continue
                x = tx * TILE_SIZE - camera_x
                y = ty * TILE_SIZE
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                color = _TILE_COLORS.get(tile_id, HARD_GRAY)
                pygame.draw.rect(surface, color, rect)

                if tile_id == TILE_QUESTION:
                    pygame.draw.rect(surface, BLACK, rect, 1)
                    cx, cy = rect.centerx, rect.centery
                    pygame.draw.line(surface, BLACK, (cx - 2, cy + 2), (cx + 2, cy - 2), 2)
                    pygame.draw.line(surface, BLACK, (cx + 2, cy - 2), (cx, cy - 2), 2)
                elif tile_id == TILE_BRICK:
                    pygame.draw.rect(surface, BLACK, rect, 1)
                    mid_y = rect.centery
                    pygame.draw.line(surface, BLACK, (rect.left, mid_y), (rect.right, mid_y))
                    pygame.draw.line(surface, BLACK, (rect.centerx, rect.top), (rect.centerx, mid_y))
                    pygame.draw.line(surface, BLACK, (rect.left + 4, mid_y), (rect.left + 4, rect.bottom))
                    pygame.draw.line(surface, BLACK, (rect.right - 4, mid_y), (rect.right - 4, rect.bottom))
                elif tile_id == TILE_HARD:
                    pygame.draw.rect(surface, BLACK, rect, 1)
                elif tile_id == TILE_USED:
                    pygame.draw.rect(surface, BLACK, rect, 1)
                elif tile_id == TILE_LAVA:
                    pygame.draw.rect(surface, BLACK, rect, 1)


_TILE_COLORS = {
    TILE_HARD: HARD_GRAY,
    TILE_BRICK: BRICK_ORANGE,
    TILE_QUESTION: QUESTION_YELLOW,
    TILE_USED: USED_BROWN,
    TILE_HIDDEN: HARD_GRAY,
    TILE_LAVA: LAVA_RED,
}
