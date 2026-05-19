import pygame
from src.physics.physics import PhysicsBody
from src.core.constants import GRAVITY, MAX_FALL, FIREBALL_SPEED, MAX_FIREBALLS


class Fireball(PhysicsBody):
    def __init__(self, x, y, facing_right):
        super().__init__(x, y, 8, 8)
        self.vx = FIREBALL_SPEED if facing_right else -FIREBALL_SPEED
        self.vy = -2.0
        self.alive = True
        self.bounces = 0

    def update(self, tile_map, collision_resolve_x, collision_resolve_y):
        self.vy += GRAVITY
        if self.vy > MAX_FALL:
            self.vy = MAX_FALL

        old_vx = self.vx
        self.x += self.vx
        collision_resolve_x(self, tile_map)
        if self.vx == 0 and old_vx != 0:
            self.alive = False
            return

        old_vy = self.vy
        self.y += self.vy
        collision_resolve_y(self, tile_map)
        if self.on_ground and old_vy > 0:
            self.vy = -2.5
            self.bounces += 1
            if self.bounces >= 3:
                self.alive = False

        if self.y > 260:
            self.alive = False

    def draw(self, surface, camera_x):
        x = int(self.x) - camera_x
        y = int(self.y)
        pygame.draw.rect(surface, (255, 100, 0), (x, y, 8, 8))
        pygame.draw.rect(surface, (255, 200, 50), (x + 2, y + 2, 4, 4))

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
