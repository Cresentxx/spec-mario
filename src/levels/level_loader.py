import json
from src.levels.tile_map import TileMap
from src.core.constants import TILE_SIZE, LEVEL_TIME


class LevelData:
    def __init__(self):
        self.world = 1
        self.level = 1
        self.theme = "overworld"
        self.time_limit = LEVEL_TIME
        self.tile_map = None
        self.player_start = (40, 192)
        self.entities = []
        self.blocks = []
        self.flagpole = None


def load_level(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    ld = LevelData()
    ld.world = data.get("world", 1)
    ld.level = data.get("level", 1)
    ld.theme = data.get("theme", "overworld")
    ld.time_limit = data.get("time_limit", LEVEL_TIME)

    tiles = data.get("tiles", [])
    width = data.get("width", len(tiles[0]) if tiles else 16)
    height = data.get("height", len(tiles))
    ld.tile_map = TileMap(tiles, width, height)

    ld.player_start = tuple(data.get("player_start", [40, 192]))
    ld.entities = data.get("entities", [])
    ld.blocks = data.get("blocks", [])
    ld.flagpole = data.get("flagpole")

    return ld
