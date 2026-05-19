import pygame
from src.core.constants import GRAVITY, MAX_FALL, JUMP_VEL, JUMP_CUT


class PhysicsBody:
    def __init__(self, x, y, w, h):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.width = w
        self.height = h
        self.on_ground = False

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    @rect.setter
    def rect(self, r):
        self.x = float(r.x)
        self.y = float(r.y)

    def apply_gravity(self):
        self.vy += GRAVITY
        if self.vy > MAX_FALL:
            self.vy = MAX_FALL

    def move_x(self):
        self.x += self.vx

    def move_y(self):
        self.y += self.vy
