import pygame
from src.core.constants import TILE_SIZE


class Pipe:
    def __init__(self, x, y, height=2, leads_to=None):
        self.x = x
        self.y = y
        self.height = height
        self.leads_to = leads_to

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, 32, self.height * TILE_SIZE)

    def can_enter(self, player_rect, input_down):
        top_rect = pygame.Rect(self.x, self.y, 32, TILE_SIZE)
        return (input_down and top_rect.colliderect(player_rect)
                and self.leads_to is not None)

    def draw(self, surface, camera_x):
        x = self.x - camera_x
        y = self.y
        h = self.height * TILE_SIZE
        # Pipe body
        pygame.draw.rect(surface, (56, 160, 56), (x, y, 32, h))
        # Pipe lip (top)
        pygame.draw.rect(surface, (56, 160, 56), (x - 2, y, 36, TILE_SIZE))
        pygame.draw.rect(surface, (0, 120, 0), (x, y, 32, TILE_SIZE), 1)
        # Highlight
        pygame.draw.rect(surface, (100, 200, 100), (x + 2, y + TILE_SIZE, 4, h - TILE_SIZE))
        # Border
        pygame.draw.rect(surface, (0, 100, 0), (x, y, 32, h), 1)
