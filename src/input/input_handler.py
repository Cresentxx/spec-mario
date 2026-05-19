import pygame
from src.core.constants import (
    SCREEN_W, SCREEN_H, WIN_W, WIN_H, FPS, STATE_TITLE, STATE_PLAYING
)


class InputHandler:
    ACTION_LEFT = "left"
    ACTION_RIGHT = "right"
    ACTION_JUMP = "jump"
    ACTION_RUN = "run"
    ACTION_PAUSE = "pause"

    _KEY_MAP = {
        pygame.K_LEFT: "left",
        pygame.K_RIGHT: "right",
        pygame.K_UP: "jump",
        pygame.K_z: "jump",
        pygame.K_SPACE: "jump",
        pygame.K_a: "left",
        pygame.K_d: "right",
        pygame.K_LSHIFT: "run",
        pygame.K_RSHIFT: "run",
        pygame.K_RETURN: "pause",
        pygame.K_p: "pause",
    }

    def __init__(self):
        self.held = set()
        self.pressed = set()
        self.released = set()

    def update(self, events):
        self.pressed.clear()
        self.released.clear()
        for event in events:
            if event.type == pygame.KEYDOWN:
                action = self._KEY_MAP.get(event.key)
                if action:
                    self.held.add(action)
                    self.pressed.add(action)
            elif event.type == pygame.KEYUP:
                action = self._KEY_MAP.get(event.key)
                if action:
                    self.held.discard(action)
                    self.released.add(action)

    def is_held(self, action):
        return action in self.held

    def just_pressed(self, action):
        return action in self.pressed

    def just_released(self, action):
        return action in self.released
