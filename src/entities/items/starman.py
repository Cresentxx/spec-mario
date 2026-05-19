import pygame
from src.physics.physics import PhysicsBody
from src.core.constants import TILE_SIZE, GRAVITY, MAX_FALL


class Starman(PhysicsBody):
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.vx = 1.5
        self.vy = -3.0
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

        if self.on_ground:
            self.vy = -3.0

    def draw(self, surface, camera_x):
        x = int(self.x) - camera_x
        y = int(self.y)
        pygame.draw.rect(surface, (255, 220, 60), (x + 2, y + 2, 12, 12))
        pygame.draw.rect(surface, (255, 255, 255), (x + 6, y + 4, 4, 8))

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
