import pygame
from src.entities.enemies.base import Enemy


class BuzzyBeetle(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 16, 16)
        self.speed = 0.5
        self.score_value = 100
        self.fire_immune = True

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
        pygame.draw.ellipse(surface, (0, 0, 180), (x, y, 16, 16))
        pygame.draw.ellipse(surface, (0, 0, 120), (x + 2, y + 2, 12, 12))
        # Head peeking
        hx = x + 10 if self.direction > 0 else x
        pygame.draw.rect(surface, (0, 0, 180), (hx, y + 2, 6, 6))
