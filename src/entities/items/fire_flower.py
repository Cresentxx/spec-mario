import pygame
from src.core.constants import TILE_SIZE, WHITE


class FireFlower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.spawn_timer = 16

    def update(self):
        if self.spawn_timer > 0:
            self.spawn_timer -= 1

    def draw(self, surface, camera_x):
        if self.spawn_timer > 0:
            return
        x = int(self.x) - camera_x
        y = int(self.y)
        pygame.draw.rect(surface, (227, 57, 57), (x + 2, y, 12, 6))
        pygame.draw.rect(surface, (255, 200, 0), (x + 4, y + 6, 8, 6))
        pygame.draw.rect(surface, WHITE, (x + 6, y + 12, 4, 4))

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), TILE_SIZE, TILE_SIZE)
