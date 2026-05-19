import pygame
import sys
import os
from src.core.constants import (
    SCREEN_W, SCREEN_H, WIN_W, WIN_H, FPS,
    STATE_PLAYING, STATE_PAUSED, STATE_DYING, STATE_GAME_OVER,
    FORM_SMALL, FORM_SUPER, FORM_FIRE,
    TILE_SIZE, TILE_QUESTION, TILE_BRICK, TILE_USED, TILE_AIR,
    INITIAL_LIVES, LEVEL_TIME, COINS_PER_LIFE,
    SKY_BLUE, BLACK, WHITE,
)
from src.input.input_handler import InputHandler
from src.core.camera import Camera
from src.entities.player import Player
from src.entities.objects.block import BlockManager
from src.entities.items.mushroom import Mushroom
from src.entities.items.fire_flower import FireFlower
from src.entities.items.starman import Starman
from src.entities.items.coin import CoinEffect
from src.levels.level_loader import load_level
from src.physics.collision import resolve_collisions_x, resolve_collisions_y


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption("Super Mario Bros.")
        self.clock = pygame.time.Clock()
        self.input = InputHandler()

        self.logic_surface = pygame.Surface((SCREEN_W, SCREEN_H))
        self.font = pygame.font.Font(None, 16)

        self.status = STATE_PLAYING
        self._load_level()

    def _level_path(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base, "levels", "data", "test.json")

    def _load_level(self):
        path = self._level_path()
        self.level_data = load_level(path)
        self.tile_map = self.level_data.tile_map
        self.player = Player(*self.level_data.player_start)
        self.player.lives = getattr(self, '_lives', INITIAL_LIVES)
        self.player.score = getattr(self, '_score', 0)
        self.player.coins = getattr(self, '_coins', 0)
        self.camera = Camera(self.tile_map.pixel_width)
        self.block_manager = BlockManager(self.level_data.blocks)
        self.items = []
        self.effects = []
        self.time_remaining = self.level_data.time_limit
        self.time_counter = 0

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.input.update(events)

            if self.input.just_pressed("pause") and self.status == STATE_PLAYING:
                self.status = STATE_PAUSED
                continue
            if self.input.just_pressed("pause") and self.status == STATE_PAUSED:
                self.status = STATE_PLAYING

            if self.status == STATE_PLAYING:
                self._update()

            self._draw()
            pygame.display.flip()
            self.clock.tick(FPS)

    def _hit_block(self, tx, ty):
        self.block_manager.hit_block(tx, ty, self.player.form, self.tile_map)

    def _update(self):
        def on_hit_block(tx, ty):
            result = self.block_manager.hit_block(tx, ty, self.player.form, self.tile_map)
            if result:
                action, content, bx, by = result
                px = bx * TILE_SIZE
                py = by * TILE_SIZE
                if action == "spawn":
                    if content == "mushroom":
                        self.items.append(Mushroom(px, py, is_1up=False))
                    elif content == "fire_flower":
                        self.items.append(FireFlower(px, py))
                    elif content == "starman":
                        self.items.append(Starman(px, py))
                    elif content == "coin":
                        self.effects.append(CoinEffect(px, py - TILE_SIZE))
                        self.player.coins += 1
                        self.player.score += 200
                    elif content == "1up":
                        self.items.append(Mushroom(px, py, is_1up=True))

        self.player.update(self.input, self.tile_map, resolve_collisions_x, resolve_collisions_y, on_hit_block)
        self.block_manager.update()

        # Update items
        for item in self.items:
            item.update(self.tile_map, resolve_collisions_x, resolve_collisions_y)
            if not item.alive:
                continue
            pr = self.player.get_hitbox()
            ir = item.get_rect()
            if pr.colliderect(ir):
                item.alive = False
                if isinstance(item, Mushroom):
                    if item.is_1up:
                        self.player.lives += 1
                    else:
                        if self.player.form == FORM_SMALL:
                            self.player.set_form(FORM_SUPER)
                        self.player.score += 1000
                elif isinstance(item, FireFlower):
                    self.player.set_form(FORM_FIRE)
                    self.player.score += 1000
                elif isinstance(item, Starman):
                    self.player.invincible = True
                    self.player.invincible_timer = INVINCIBLE_FRAMES
                    self.player.score += 1000
        self.items = [i for i in self.items if i.alive]

        # Update effects
        for eff in self.effects:
            eff.update()
        self.effects = [e for e in self.effects if e.alive]

        # Timer
        self.time_counter += 1
        if self.time_counter >= FPS:
            self.time_counter = 0
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.player.die()

        # Camera
        self.camera.update(self.player.x)

        # Check coin lives
        if self.player.coins >= COINS_PER_LIFE:
            self.player.coins -= COINS_PER_LIFE
            self.player.lives += 1

        # Handle death
        if self.player.dead and self.player.death_timer <= 0:
            self._lives = self.player.lives - 1
            self._score = self.player.score
            self._coins = self.player.coins
            if self._lives <= 0:
                self.status = STATE_GAME_OVER
            else:
                self._load_level()

    def _draw(self):
        surf = self.logic_surface
        surf.fill(SKY_BLUE if self.level_data.theme == "overworld" else BLACK)

        if self.status == STATE_GAME_OVER:
            self._draw_game_over(surf)
            scaled = pygame.transform.scale(surf, (WIN_W, WIN_H))
            self.screen.blit(scaled, (0, 0))
            return

        self.tile_map.draw(surf, self.camera.offset_x)

        # Draw block bounce offsets
        for (tx, ty), info in self.block_manager.blocks.items():
            offset = self.block_manager.get_bounce_offset(tx, ty)
            if offset != 0:
                tile_id = self.tile_map.get_tile(tx, ty)
                if tile_id != TILE_AIR:
                    x = tx * TILE_SIZE - self.camera.offset_x
                    y = ty * TILE_SIZE + offset
                    from src.levels.tile_map import _TILE_COLORS
                    color = _TILE_COLORS.get(tile_id, (130, 130, 130))
                    pygame.draw.rect(surf, color, (x, y, TILE_SIZE, TILE_SIZE))

        for item in self.items:
            item.draw(surf, self.camera.offset_x)
        for eff in self.effects:
            eff.draw(surf, self.camera.offset_x)

        self.player.draw(surf, self.camera.offset_x)

        self._draw_hud(surf)

        if self.status == STATE_PAUSED:
            overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            surf.blit(overlay, (0, 0))
            text = self.font.render("PAUSED", True, WHITE)
            surf.blit(text, (SCREEN_W // 2 - text.get_width() // 2, SCREEN_H // 2 - 4))

        scaled = pygame.transform.scale(surf, (WIN_W, WIN_H))
        self.screen.blit(scaled, (0, 0))

    def _draw_hud(self, surf):
        score_str = f"{self.player.score:06d}"
        coins_str = f"{self.player.coins:02d}"
        world_str = f"{self.level_data.world}-{self.level_data.level}"
        time_str = f"{self.time_remaining:03d}"

        y = 2
        self._draw_text(surf, "MARIO", 8, y)
        self._draw_text(surf, score_str, 8, y + 10)

        self._draw_text(surf, "x" + coins_str, 80, y + 10)

        self._draw_text(surf, "WORLD", 140, y)
        self._draw_text(surf, world_str, 148, y + 10)

        self._draw_text(surf, "TIME", 200, y)
        self._draw_text(surf, time_str, 206, y + 10)

    def _draw_text(self, surf, text, x, y):
        rendered = self.font.render(text, True, WHITE)
        surf.blit(rendered, (x, y))

    def _draw_game_over(self, surf):
        surf.fill(BLACK)
        text = self.font.render("GAME OVER", True, WHITE)
        surf.blit(text, (SCREEN_W // 2 - text.get_width() // 2, SCREEN_H // 2 - 4))
