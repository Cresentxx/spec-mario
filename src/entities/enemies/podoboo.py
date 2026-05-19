import pygame
import math


class Podoboo:
    def __init__(self, x, y):
        self.base_y = float(y)
        self.x = float(x)
        self.y = float(y)
        self.alive = True
        self.score_value = 200
        self.width = 16
        self.height = 16
        self.timer = 0
        self.period = 120
        self.jump_height = 48

    def update(self):
        self.timer += 1
        phase = self.timer % self.period
        if phase < 40:
            t = phase / 40.0
            self.y = self.base_y - self.jump_height * math.sin(t * math.pi)
        else:
            self.y = self.base_y

    def draw(self, surface, camera_x):
        if not self.alive:
            return
        x = int(self.x) - camera_x
        y = int(self.y)
        if y >= self.base_y:
            return
        pygame.draw.circle(surface, (255, 80, 0), (x + 8, y + 8), 8)
        pygame.draw.circle(surface, (255, 200, 50), (x + 8, y + 6), 4)

    def get_rect(self):
        if self.y >= self.base_y:
            return pygame.Rect(0, 0, 0, 0)
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
