import pygame
from src.core.constants import COIN_GOLD, WHITE


class EffectManager:
    def __init__(self):
        self.effects = []

    def add(self, effect):
        self.effects.append(effect)

    def add_brick_debris(self, x, y):
        for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
            self.effects.append(BrickDebris(x, y, dx * 1.5, dy * 3.0))

    def add_score_popup(self, x, y, score):
        self.effects.append(ScorePopup(x, y, score))

    def add_coin_effect(self, x, y):
        self.effects.append(CoinPopup(x, y))

    def update(self):
        for e in self.effects:
            e.update()
        self.effects = [e for e in self.effects if e.alive]

    def draw(self, surface, camera_x):
        for e in self.effects:
            e.draw(surface, camera_x)


class BrickDebris:
    def __init__(self, x, y, vx, vy):
        self.x = float(x)
        self.y = float(y)
        self.vx = vx
        self.vy = vy
        self.alive = True
        self.timer = 40

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.25
        self.timer -= 1
        if self.timer <= 0:
            self.alive = False

    def draw(self, surface, camera_x):
        x = int(self.x) - camera_x
        y = int(self.y)
        pygame.draw.rect(surface, (191, 99, 43), (x, y, 6, 6))


class ScorePopup:
    def __init__(self, x, y, score):
        self.x = x
        self.y = float(y)
        self.score = score
        self.alive = True
        self.timer = 30
        self.font = pygame.font.Font(None, 14)

    def update(self):
        self.y -= 0.5
        self.timer -= 1
        if self.timer <= 0:
            self.alive = False

    def draw(self, surface, camera_x):
        x = int(self.x) - camera_x
        y = int(self.y)
        text = self.font.render(str(self.score), True, WHITE)
        surface.blit(text, (x, y))


class CoinPopup:
    def __init__(self, x, y):
        self.x = x
        self.y = float(y)
        self.vy = -4.0
        self.alive = True
        self.timer = 20

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
