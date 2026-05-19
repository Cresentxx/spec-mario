import pygame
from src.physics.physics import PhysicsBody
from src.core.constants import TILE_SIZE, GRAVITY, MAX_FALL, WHITE


class Mushroom(PhysicsBody):
    def __init__(self, x, y, is_1up=False):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.vx = 1.0
        self.vy = 0.0
        self.is_1up = is_1up
        self.alive = True
        self.spawn_rise = TILE_SIZE
        self.spawning = True
        self.spawn_target_y = y - TILE_SIZE

    def update(self, tile_map, collision_resolve_x, collision_resolve_y):
        if self.spawning:
            self.y -= 1
            if self.y <= self.spawn_target_y:
                self.y = self.spawn_target_y
                self.spawning = False
            return

        self.vy += GRAVITY
        if self.vy > MAX_FALL:
            self.vy = MAX_FALL

        self.x += self.vx
        collision_resolve_x(self, tile_map)
        self.y += self.vy
        collision_resolve_y(self, tile_map)

    def draw(self, surface, camera_x):
        x = int(self.x) - camera_x
        y = int(self.y)
        color = (56, 160, 56) if self.is_1up else (227, 57, 57)
        pygame.draw.rect(surface, color, (x + 2, y, 12, TILE_SIZE))
        pygame.draw.rect(surface, WHITE if not self.is_1up else (200, 255, 200), (x + 4, y + 4, 8, 4))

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
