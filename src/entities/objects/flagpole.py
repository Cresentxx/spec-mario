import pygame
from src.core.constants import SCREEN_H


class Flagpole:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = SCREEN_H - y - 16
        self.triggered = False
        self.slide_y = 0
        self.slide_speed = 2.0

    def get_trigger_rect(self):
        return pygame.Rect(self.x - 4, self.y, 8, self.height)

    def trigger(self, player_y):
        self.triggered = True
        rel = (player_y - self.y) / max(1, self.height)
        rel = max(0, min(1, rel))
        if rel < 0.2:
            return 5000
        elif rel < 0.4:
            return 2000 + int((1 - rel) * 5000)
        elif rel < 0.7:
            return 400 + int((1 - rel) * 2000)
        else:
            return 100

    def draw(self, surface, camera_x):
        x = self.x - camera_x
        y = self.y
        # Pole
        pygame.draw.rect(surface, (150, 150, 150), (x, y, 2, self.height))
        # Ball on top
        pygame.draw.circle(surface, (200, 200, 200), (x + 1, y), 4)
        # Flag
        flag_y = y + 8 + int(self.slide_y)
        if not self.triggered:
            pygame.draw.polygon(surface, (56, 160, 56),
                                [(x + 2, flag_y), (x + 14, flag_y + 6), (x + 2, flag_y + 12)])
