import math
import pygame


class MovingPlatform:
    def __init__(self, x, y, width=48, height=8, move_range=64, speed=0.5, vertical=False):
        self.start_x = float(x)
        self.start_y = float(y)
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height
        self.move_range = move_range
        self.speed = speed
        self.vertical = vertical
        self.timer = 0.0

    def update(self):
        self.timer += self.speed
        if self.vertical:
            self.y = self.start_y + math.sin(self.timer * 0.03) * self.move_range
        else:
            self.x = self.start_x + math.sin(self.timer * 0.03) * self.move_range

    @property
    def dx(self):
        return math.cos(self.timer * 0.03) * self.speed * 0.03 * self.move_range

    @property
    def dy(self):
        if self.vertical:
            return math.cos(self.timer * 0.03) * self.speed * 0.03 * self.move_range
        return 0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, surface, camera_x):
        x = int(self.x) - camera_x
        y = int(self.y)
        pygame.draw.rect(surface, (180, 120, 60), (x, y, self.width, self.height))
        pygame.draw.rect(surface, (140, 90, 40), (x, y, self.width, self.height), 1)
