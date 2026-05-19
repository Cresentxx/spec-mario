import pygame
from src.core.constants import GRAVITY, MAX_FALL, TILE_SIZE, SOLID_TILES


class Bowser:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.width = 32
        self.height = 32
        self.alive = True
        self.hp = 5
        self.score_value = 5000
        self.direction = -1
        self.speed = 0.5
        self.on_ground = False
        self.jump_timer = 0
        self.jump_interval = 120
        self.fire_timer = 0
        self.fire_interval = 90
        self.hammers = []
        self.hammer_timer = 0
        self.hammer_interval = 150
        self.fireballs = []

    def update(self, tile_map):
        if not self.alive:
            return

        # Movement
        self.vx = self.direction * self.speed
        self.vy += GRAVITY
        if self.vy > MAX_FALL:
            self.vy = MAX_FALL

        # Jump
        self.jump_timer += 1
        if self.jump_timer >= self.jump_interval and self.on_ground:
            self.vy = -5.5
            self.jump_timer = 0

        # Reverse at edges
        self.x += self.vx
        self._resolve_x(tile_map)

        self.on_ground = False
        self.y += self.vy
        self._resolve_y(tile_map)

        # Fire
        self.fire_timer += 1
        if self.fire_timer >= self.fire_interval:
            self.fire_timer = 0
            self.fireballs.append(BowserFireball(self.x, self.y + 8, self.direction))

        for f in self.fireballs:
            f.update()
        self.fireballs = [f for f in self.fireballs if f.alive]

        if self.y > 280:
            self.alive = False

    def _resolve_x(self, tile_map):
        left_tile = max(0, int(self.x) // TILE_SIZE)
        right_tile = min(tile_map.width - 1, int(self.x + self.width) // TILE_SIZE)
        top_tile = max(0, int(self.y) // TILE_SIZE)
        bot_tile = min(tile_map.height - 1, int(self.y + self.height) // TILE_SIZE)
        for ty in range(top_tile, bot_tile + 1):
            for tx in range(left_tile, right_tile + 1):
                if tile_map.get_tile(tx, ty) in SOLID_TILES:
                    tl = tx * TILE_SIZE
                    tr = tl + TILE_SIZE
                    tt = ty * TILE_SIZE
                    tb = tt + TILE_SIZE
                    if (self.x + self.width > tl and self.x < tr and
                            self.y + self.height > tt and self.y < tb):
                        if self.vx > 0:
                            self.x = tl - self.width
                        elif self.vx < 0:
                            self.x = tr
                        self.direction *= -1
                        self.vx = 0
                        return

    def _resolve_y(self, tile_map):
        left_tile = max(0, int(self.x) // TILE_SIZE)
        right_tile = min(tile_map.width - 1, int(self.x + self.width) // TILE_SIZE)
        top_tile = max(0, int(self.y) // TILE_SIZE)
        bot_tile = min(tile_map.height - 1, int(self.y + self.height) // TILE_SIZE)
        for ty in range(top_tile, bot_tile + 1):
            for tx in range(left_tile, right_tile + 1):
                if tile_map.get_tile(tx, ty) in SOLID_TILES:
                    tl = tx * TILE_SIZE
                    tt = ty * TILE_SIZE
                    tb = tt + TILE_SIZE
                    if (self.x + self.width > tl and self.x < tl + TILE_SIZE and
                            self.y + self.height > tt and self.y < tb):
                        if self.vy >= 0:
                            self.y = tt - self.height
                            self.vy = 0
                            self.on_ground = True
                        elif self.vy < 0:
                            self.y = tb
                            self.vy = 0

    def hit_by_fireball(self):
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False
            return self.score_value
        return 0

    def draw(self, surface, camera_x):
        if not self.alive:
            return
        x = int(self.x) - camera_x
        y = int(self.y)
        # Body
        pygame.draw.rect(surface, (56, 160, 56), (x + 4, y + 8, 24, 20))
        # Shell
        pygame.draw.rect(surface, (200, 150, 50), (x + 6, y + 10, 20, 14))
        # Head
        hx = x + 22 if self.direction < 0 else x
        pygame.draw.rect(surface, (56, 160, 56), (hx, y, 14, 14))
        # Eyes
        ex = hx + 8
        pygame.draw.rect(surface, (255, 255, 255), (ex, y + 3, 4, 4))
        pygame.draw.rect(surface, (255, 0, 0), (ex + 1, y + 4, 2, 2))
        # Horns
        pygame.draw.rect(surface, (200, 150, 50), (x + 4, y - 4, 4, 6))
        pygame.draw.rect(surface, (200, 150, 50), (x + 24, y - 4, 4, 6))
        # Mouth
        pygame.draw.rect(surface, (200, 60, 60), (hx + 2, y + 10, 10, 4))

        for f in self.fireballs:
            f.draw(surface, camera_x)

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)


class BowserFireball:
    def __init__(self, x, y, direction):
        self.x = float(x)
        self.y = float(y)
        self.vx = -2.0 if direction < 0 else 2.0
        self.alive = True
        self.timer = 180

    def update(self):
        self.x += self.vx
        self.timer -= 1
        if self.timer <= 0:
            self.alive = False

    def draw(self, surface, camera_x):
        x = int(self.x) - camera_x
        y = int(self.y)
        pygame.draw.rect(surface, (255, 80, 0), (x, y, 8, 8))
        pygame.draw.rect(surface, (255, 200, 50), (x + 2, y + 2, 4, 4))

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), 8, 8)
