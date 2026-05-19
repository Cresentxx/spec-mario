import pygame
from src.entities.enemies.base import Enemy


class KoopaGreen(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 16, 24)
        self.speed = 0.5
        self.score_value = 100

    def update(self, tile_map, collision_resolve_x, collision_resolve_y):
        if not self.alive:
            return

        self.vx = self.direction * self.speed
        self.vy += 0.25
        if self.vy > 4.5:
            self.vy = 4.5

        old_vx = self.vx
        self.x += self.vx
        collision_resolve_x(self, tile_map)
        if self.vx == 0 and old_vx != 0:
            self.direction *= -1

        self.y += self.vy
        collision_resolve_y(self, tile_map)

        if self.y > 260:
            self.alive = False

    def _draw_body(self, surface, x, y):
        # Shell
        pygame.draw.rect(surface, (56, 160, 56), (x, y + 8, 16, 14))
        pygame.draw.rect(surface, (0, 100, 0), (x + 2, y + 10, 12, 10))
        # Head
        pygame.draw.rect(surface, (255, 220, 150), (x + 2, y, 12, 10))
        # Eye
        ex = x + 8 if self.direction > 0 else x + 4
        pygame.draw.rect(surface, (0, 0, 0), (ex, y + 2, 3, 3))
        # Feet
        pygame.draw.rect(surface, (255, 220, 150), (x, y + 22, 6, 2))
        pygame.draw.rect(surface, (255, 220, 150), (x + 10, y + 22, 6, 2))
