import math
import pygame


class FireBar:
    def __init__(self, cx, cy, length=4, speed=0.02):
        self.cx = cx
        self.cy = cy
        self.length = length
        self.speed = speed
        self.angle = 0.0

    def update(self):
        self.angle += self.speed

    def get_segments(self):
        segments = []
        for i in range(self.length):
            r = 8 + i * 8
            x = self.cx + math.cos(self.angle) * r
            y = self.cy + math.sin(self.angle) * r
            segments.append(pygame.Rect(int(x) - 4, int(y) - 4, 8, 8))
        return segments

    def draw(self, surface, camera_x):
        for seg in self.get_segments():
            x = seg.x - camera_x
            pygame.draw.rect(surface, (255, 100, 0), (x, seg.y, 8, 8))
            pygame.draw.rect(surface, (255, 200, 50), (x + 2, seg.y + 2, 4, 4))
        # Center
        pygame.draw.circle(surface, (100, 100, 100),
                           (self.cx - camera_x, self.cy), 4)
