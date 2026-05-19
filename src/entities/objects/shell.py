import pygame
from src.core.constants import TILE_SIZE, GRAVITY, MAX_FALL, SOLID_TILES


class Shell:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.width = 16
        self.height = 14
        self.alive = True
        self.moving = False
        self.combo_count = 0
        self.score_values = [200, 400, 800, 1000, 2000, 4000, 8000]
        self.on_ground = False

    def kick(self, direction):
        self.moving = True
        self.vx = 4.0 * direction

    def update(self, tile_map, collision_resolve_x, collision_resolve_y):
        if not self.alive:
            return

        if self.moving:
            self.vy += GRAVITY
            if self.vy > MAX_FALL:
                self.vy = MAX_FALL

            old_vx = self.vx
            self.x += self.vx
            collision_resolve_x_shell(self, tile_map)
            if self.vx == 0 and old_vx != 0:
                self.vx = -old_vx

            self.y += self.vy
            collision_resolve_y_shell(self, tile_map)

        if self.y > 260:
            self.alive = False

    def get_kill_score(self):
        if self.combo_count < len(self.score_values):
            score = self.score_values[self.combo_count]
        else:
            score = 0
        self.combo_count += 1
        return score if score > 0 else 0

    def draw(self, surface, camera_x):
        if not self.alive:
            return
        x = int(self.x) - camera_x
        y = int(self.y)
        pygame.draw.rect(surface, (56, 160, 56), (x, y, 16, 14))
        pygame.draw.rect(surface, (0, 100, 0), (x + 2, y + 2, 12, 10))
        pygame.draw.rect(surface, (56, 160, 56), (x + 4, y + 4, 8, 6))

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)


def collision_resolve_x_shell(shell, tile_map):
    left_tile = max(0, int(shell.x) // TILE_SIZE)
    right_tile = min(tile_map.width - 1, int(shell.x + shell.width) // TILE_SIZE)
    top_tile = max(0, int(shell.y) // TILE_SIZE)
    bot_tile = min(tile_map.height - 1, int(shell.y + shell.height) // TILE_SIZE)

    for ty in range(top_tile, bot_tile + 1):
        for tx in range(left_tile, right_tile + 1):
            if tile_map.get_tile(tx, ty) in SOLID_TILES:
                tile_left = tx * TILE_SIZE
                tile_right = tile_left + TILE_SIZE
                tile_top = ty * TILE_SIZE
                tile_bottom = tile_top + TILE_SIZE
                if (shell.x + shell.width > tile_left and shell.x < tile_right and
                        shell.y + shell.height > tile_top and shell.y < tile_bottom):
                    if shell.vx > 0:
                        shell.x = tile_left - shell.width
                    elif shell.vx < 0:
                        shell.x = tile_right
                    shell.vx = -shell.vx
                    return


def collision_resolve_y_shell(shell, tile_map):
    shell.on_ground = False
    left_tile = max(0, int(shell.x) // TILE_SIZE)
    right_tile = min(tile_map.width - 1, int(shell.x + shell.width) // TILE_SIZE)
    top_tile = max(0, int(shell.y) // TILE_SIZE)
    bot_tile = min(tile_map.height - 1, int(shell.y + shell.height) // TILE_SIZE)

    for ty in range(top_tile, bot_tile + 1):
        for tx in range(left_tile, right_tile + 1):
            if tile_map.get_tile(tx, ty) in SOLID_TILES:
                tile_left = tx * TILE_SIZE
                tile_top = ty * TILE_SIZE
                tile_bottom = tile_top + TILE_SIZE
                if (shell.x + shell.width > tile_left and shell.x < tile_left + TILE_SIZE and
                        shell.y + shell.height > tile_top and shell.y < tile_bottom):
                    if shell.vy >= 0:
                        shell.y = tile_top - shell.height
                        shell.vy = 0
                        shell.on_ground = True
                    elif shell.vy < 0:
                        shell.y = tile_bottom
                        shell.vy = 0
