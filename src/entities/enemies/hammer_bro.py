import pygame
from src.entities.enemies.base import Enemy
from src.core.constants import GRAVITY, MAX_FALL


class HammerBro(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 16, 24)
        self.speed = 0.3
        self.hp = 2
        self.score_value = 1000
        self.hammer_timer = 0
        self.hammer_interval = 90
        self.hammers = []
        self.jump_timer = 0
        self.jump_interval = 120
        self.jumping = False

    def update(self, tile_map, collision_resolve_x, collision_resolve_y):
        if not self.alive:
            return

        self.vx = self.direction * self.speed
        self.vy += GRAVITY
        if self.vy > MAX_FALL:
            self.vy = MAX_FALL

        # Jump periodically
        self.jump_timer += 1
        if self.jump_timer >= self.jump_interval and self.on_ground:
            self.vy = -5.0
            self.jump_timer = 0
            self.direction *= -1

        old_vx = self.vx
        self.x += self.vx
        collision_resolve_x(self, tile_map)
        if self.vx == 0 and old_vx != 0:
            self.direction *= -1

        self.y += self.vy
        collision_resolve_y(self, tile_map)

        # Throw hammers
        self.hammer_timer += 1
        if self.hammer_timer >= self.hammer_interval:
            self.hammer_timer = 0
            self.hammers.append(Hammer(self.x, self.y, self.direction))

        for h in self.hammers:
            h.update(tile_map)
        self.hammers = [h for h in self.hammers if h.alive]

        if self.y > 260:
            self.alive = False

    def hit_by_fireball(self):
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False
            self.hammers.clear()
            return self.score_value
        return 0

    def _draw_body(self, surface, camera_x_offset=0):
        pass

    def draw(self, surface, camera_x):
        if not self.alive:
            return
        x = int(self.x) - camera_x
        y = int(self.y)
        # Body
        pygame.draw.rect(surface, (56, 160, 56), (x, y + 8, 16, 16))
        # Head
        pygame.draw.rect(surface, (255, 220, 150), (x + 2, y, 12, 10))
        # Helmet
        pygame.draw.rect(surface, (56, 160, 56), (x, y - 2, 16, 4))
        # Eyes
        ex = x + 8 if self.direction > 0 else x + 4
        pygame.draw.rect(surface, (0, 0, 0), (ex, y + 3, 3, 3))
        # Feet
        pygame.draw.rect(surface, (0, 0, 0), (x, y + 22, 6, 2))
        pygame.draw.rect(surface, (0, 0, 0), (x + 10, y + 22, 6, 2))
        # Draw hammers
        for h in self.hammers:
            h.draw(surface, camera_x)


class Hammer:
    def __init__(self, x, y, direction):
        self.x = float(x)
        self.y = float(y)
        self.vx = 2.0 * direction
        self.vy = -4.0
        self.alive = True
        self.timer = 90

    def update(self, tile_map):
        self.vy += 0.2
        self.x += self.vx
        self.y += self.vy
        self.timer -= 1
        if self.timer <= 0 or self.y > 260:
            self.alive = False

    def draw(self, surface, camera_x):
        x = int(self.x) - camera_x
        y = int(self.y)
        pygame.draw.rect(surface, (139, 90, 43), (x, y, 8, 6))
        pygame.draw.rect(surface, (100, 100, 100), (x + 2, y - 3, 4, 3))

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), 8, 6)
