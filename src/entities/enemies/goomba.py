import pygame
from src.entities.enemies.base import Enemy


class Goomba(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 16, 16)
        self.speed = 0.5
        self.score_value = 100

    def update(self, tile_map, collision_resolve_x, collision_resolve_y):
        if not self.alive or self.flat_timer > 0:
            if self.flat_timer > 0:
                self.flat_timer -= 1
                if self.flat_timer <= 0:
                    self.alive = False
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
        # Body
        pygame.draw.rect(surface, (139, 90, 43), (x + 1, y + 4, 14, 10))
        # Head
        pygame.draw.rect(surface, (139, 90, 43), (x, y, 16, 8))
        # Eyes
        pygame.draw.rect(surface, (255, 255, 255), (x + 3, y + 2, 4, 4))
        pygame.draw.rect(surface, (255, 255, 255), (x + 9, y + 2, 4, 4))
        pygame.draw.rect(surface, (0, 0, 0), (x + 4, y + 3, 2, 2))
        pygame.draw.rect(surface, (0, 0, 0), (x + 10, y + 3, 2, 2))
        # Feet
        pygame.draw.rect(surface, (0, 0, 0), (x, y + 14, 6, 2))
        pygame.draw.rect(surface, (0, 0, 0), (x + 10, y + 14, 6, 2))
