import pygame
import math
from src.core.constants import SCREEN_W, GRAVITY, TILE_SIZE, SOLID_TILES


class Lakitu:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.base_x = float(x)
        self.alive = True
        self.score_value = 200
        self.width = 16
        self.height = 16
        self.timer = 0
        self.spinys = []
        self.spawn_interval = 180
        self.respawn_timer = 0
        self.active = True

    def update(self, camera_x, tile_map):
        if not self.active:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.active = True
                self.x = camera_x + SCREEN_W + 16
            return

        self.timer += 1
        self.x = self.base_x + math.sin(self.timer * 0.02) * 40
        self.base_x = max(camera_x + 30, self.base_x)
        self.base_x = min(camera_x + SCREEN_W - 30, self.base_x)

        if self.timer % self.spawn_interval == 0:
            self.spinys.append(Spiny(self.x, self.y + 16))

        for s in self.spinys:
            s.update(tile_map)
        self.spinys = [s for s in self.spinys if s.alive]

        if self.x < camera_x - 64:
            self.active = False
            self.respawn_timer = 300

    def draw(self, surface, camera_x):
        if not self.active:
            return
        x = int(self.x) - camera_x
        y = int(self.y)
        # Cloud
        pygame.draw.ellipse(surface, (255, 255, 255), (x - 4, y - 8, 24, 14))
        pygame.draw.ellipse(surface, (200, 200, 255), (x - 2, y - 6, 20, 10))
        # Lakitu body
        pygame.draw.rect(surface, (255, 255, 255), (x + 2, y + 4, 12, 10))
        pygame.draw.rect(surface, (0, 0, 0), (x + 6, y + 5, 2, 2))
        pygame.draw.rect(surface, (0, 0, 0), (x + 10, y + 5, 2, 2))
        for s in self.spinys:
            s.draw(surface, camera_x)

    def get_rect(self):
        if not self.active:
            return pygame.Rect(0, 0, 0, 0)
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)


class Spiny:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.5
        self.vy = 0
        self.alive = True
        self.score_value = 200
        self.width = 16
        self.height = 16
        self.on_ground = False
        self.no_stomp = True

    def update(self, tile_map):
        if not self.alive:
            return
        self.vy += GRAVITY
        if self.vy > 4.5:
            self.vy = 4.5
        if self.on_ground:
            self.x += self.vx

        self.on_ground = False
        self.y += self.vy

        ty = int((self.y + self.height) // TILE_SIZE)
        tx_start = max(0, int(self.x) // TILE_SIZE)
        tx_end = min(tile_map.width - 1, int(self.x + self.width) // TILE_SIZE)
        for tx in range(tx_start, tx_end + 1):
            if tile_map.get_tile(tx, ty) in SOLID_TILES:
                tile_top = ty * TILE_SIZE
                if self.y + self.height > tile_top and self.vy >= 0:
                    self.y = tile_top - self.height
                    self.vy = 0
                    self.on_ground = True
                    break

        old_vx = self.vx
        tx_check = int((self.x + (self.width + 2 if self.vx > 0 else -2)) // TILE_SIZE)
        ty_check = int((self.y + self.height + 2) // TILE_SIZE)
        if 0 <= tx_check < tile_map.width and 0 <= ty_check < tile_map.height:
            if tile_map.get_tile(tx_check, ty_check) not in SOLID_TILES:
                self.vx = -old_vx

        if self.y > 260:
            self.alive = False

    def draw(self, surface, camera_x):
        if not self.alive:
            return
        x = int(self.x) - camera_x
        y = int(self.y)
        pygame.draw.rect(surface, (200, 60, 60), (x, y + 4, 16, 12))
        # Spikes
        pygame.draw.polygon(surface, (200, 60, 60), [(x + 2, y + 4), (x, y), (x + 4, y + 4)])
        pygame.draw.polygon(surface, (200, 60, 60), [(x + 6, y + 4), (x + 6, y - 2), (x + 10, y + 4)])
        pygame.draw.polygon(surface, (200, 60, 60), [(x + 12, y + 4), (x + 16, y), (x + 14, y + 4)])
        pygame.draw.rect(surface, (0, 0, 0), (x + 4, y + 8, 2, 2))
        pygame.draw.rect(surface, (0, 0, 0), (x + 10, y + 8, 2, 2))

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
