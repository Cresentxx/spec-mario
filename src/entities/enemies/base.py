import pygame
from src.physics.physics import PhysicsBody
from src.core.constants import GRAVITY, MAX_FALL, TILE_SIZE, SOLID_TILES


class Enemy(PhysicsBody):
    def __init__(self, x, y, w=16, h=16):
        super().__init__(x, y, w, h)
        self.direction = -1
        self.speed = 0.5
        self.hp = 1
        self.score_value = 100
        self.alive = True
        self.active = True
        self.flat_timer = 0
        self.flat_duration = 20
        self.fire_immune = False

    def update(self, tile_map, collision_resolve_x, collision_resolve_y):
        if not self.alive:
            return
        if self.flat_timer > 0:
            self.flat_timer -= 1
            if self.flat_timer <= 0:
                self.alive = False
            return

        self.vx = self.direction * self.speed
        self.vy += GRAVITY
        if self.vy > MAX_FALL:
            self.vy = MAX_FALL

        old_vx = self.vx
        self.x += self.vx
        collision_resolve_x(self, tile_map)
        if self.vx == 0 and old_vx != 0:
            self.direction *= -1

        self.y += self.vy
        collision_resolve_y(self, tile_map)

        if self.y > 260:
            self.alive = False

    def stomp(self):
        self.flat_timer = self.flat_duration
        return self.score_value

    def hit_by_fireball(self):
        if self.fire_immune:
            return 0
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False
            return self.score_value
        return 0

    def check_cliff(self, tile_map):
        ahead_x = int(self.x + (self.width if self.direction > 0 else -2))
        below_y = int(self.y + self.height + 2)
        tx = ahead_x // TILE_SIZE
        ty = below_y // TILE_SIZE
        if 0 <= tx < tile_map.width and 0 <= ty < tile_map.height:
            return tile_map.get_tile(tx, ty) in SOLID_TILES
        return False

    def draw(self, surface, camera_x):
        if not self.alive:
            return
        x = int(self.x) - camera_x
        y = int(self.y)
        if self.flat_timer > 0:
            pygame.draw.rect(surface, (139, 90, 43), (x, y + 10, 16, 6))
        else:
            self._draw_body(surface, x, y)

    def _draw_body(self, surface, x, y):
        pygame.draw.rect(surface, (139, 90, 43), (x, y, 16, 16))

    def get_rect(self):
        if self.flat_timer > 0:
            return pygame.Rect(int(self.x), int(self.y) + 10, self.width, 6)
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
