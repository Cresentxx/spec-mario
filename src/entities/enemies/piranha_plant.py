import pygame
from src.core.constants import TILE_SIZE


class PiranhaPlant:
    def __init__(self, x, y):
        self.base_y = y
        self.x = x
        self.y = float(y)
        self.timer = 0
        self.period = 120
        self.alive = True
        self.score_value = 200
        self.width = 16
        self.height = 24
        self.state = "hidden"
        self.extend_speed = 0.5

    def update(self):
        if not self.alive:
            return
        self.timer += 1
        phase = self.timer % self.period
        if phase < 40:
            self.state = "rising"
            self.y = self.base_y - (phase / 40.0) * 24
        elif phase < 60:
            self.state = "up"
            self.y = self.base_y - 24
        elif phase < 100:
            self.state = "lowering"
            self.y = self.base_y - 24 + ((phase - 60) / 40.0) * 24
        else:
            self.state = "hidden"
            self.y = float(self.base_y)

    def draw(self, surface, camera_x):
        if not self.alive or self.state == "hidden":
            return
        x = int(self.x) - camera_x
        y = int(self.y)
        # Stem
        pygame.draw.rect(surface, (56, 160, 56), (x + 4, y + 8, 8, 16))
        # Head
        pygame.draw.rect(surface, (180, 30, 30), (x, y, 16, 12))
        pygame.draw.polygon(surface, (255, 255, 255),
                            [(x, y + 4), (x + 4, y), (x + 4, y + 4)])
        pygame.draw.polygon(surface, (255, 255, 255),
                            [(x + 16, y + 4), (x + 12, y), (x + 12, y + 4)])
        # Dots
        pygame.draw.rect(surface, (255, 255, 255), (x + 3, y + 3, 2, 2))
        pygame.draw.rect(surface, (255, 255, 255), (x + 11, y + 3, 2, 2))

    def get_rect(self):
        if self.state == "hidden":
            return pygame.Rect(0, 0, 0, 0)
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
