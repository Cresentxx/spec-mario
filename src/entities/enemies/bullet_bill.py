import pygame
from src.core.constants import SCREEN_W


class BulletBill:
    def __init__(self, x, y, direction=-1):
        self.x = float(x)
        self.y = float(y)
        self.vx = -1.0 if direction < 0 else 1.0
        self.alive = True
        self.score_value = 200
        self.width = 16
        self.height = 16

    def update(self, camera_x):
        self.x += self.vx
        if self.x < camera_x - 32 or self.x > camera_x + SCREEN_W + 32:
            self.alive = False

    def draw(self, surface, camera_x):
        x = int(self.x) - camera_x
        y = int(self.y)
        pygame.draw.rect(surface, (30, 30, 30), (x, y, 16, 16))
        pygame.draw.rect(surface, (255, 255, 255), (x + 2, y + 4, 4, 4))
        pygame.draw.rect(surface, (200, 60, 60), (x + 12, y + 6, 4, 4))

    def stomp(self):
        self.alive = False
        return self.score_value

    def hit_by_fireball(self):
        self.alive = False
        return self.score_value

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
