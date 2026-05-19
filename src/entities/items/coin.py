import pygame
from src.core.constants import TILE_SIZE, COIN_GOLD


class CoinEffect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = -4.0
        self.alive = True
        self.timer = 24

    def update(self):
        self.y += self.vy
        self.vy += 0.3
        self.timer -= 1
        if self.timer <= 0:
            self.alive = False

    def draw(self, surface, camera_x):
        x = int(self.x) - camera_x
        y = int(self.y)
        frame = self.timer % 4
        w = [16, 10, 4, 10][frame]
        offset = (16 - w) // 2
        pygame.draw.rect(surface, COIN_GOLD, (x + offset, y, w, 14))
