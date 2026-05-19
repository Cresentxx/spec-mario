from src.core.constants import SCREEN_W


class Camera:
    def __init__(self, level_pixel_width):
        self.x = 0.0
        self.max_x = max(0, level_pixel_width - SCREEN_W)

    def update(self, player_x):
        target = player_x - SCREEN_W * 0.4
        self.x = max(self.x, target)
        self.x = min(self.x, self.max_x)

    @property
    def offset_x(self):
        return int(self.x)
