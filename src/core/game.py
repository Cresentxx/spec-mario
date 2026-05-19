import pygame
import sys
import os
from src.core.constants import (
    SCREEN_W, SCREEN_H, WIN_W, WIN_H, FPS,
    STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER,
    FORM_SMALL, FORM_SUPER, FORM_FIRE,
    TILE_SIZE, TILE_QUESTION, TILE_BRICK, TILE_USED, TILE_AIR,
    INITIAL_LIVES, COINS_PER_LIFE, MAX_FIREBALLS, INVINCIBLE_FRAMES,
    SKY_BLUE, BLACK, WHITE,
)
from src.input.input_handler import InputHandler
from src.core.camera import Camera
from src.entities.player import Player
from src.entities.objects.block import BlockManager
from src.entities.items.mushroom import Mushroom
from src.entities.items.fire_flower import FireFlower
from src.entities.items.starman import Starman
from src.entities.items.fireball import Fireball
from src.entities.objects.shell import Shell
from src.entities.objects.pipe import Pipe
from src.entities.objects.flagpole import Flagpole
from src.entities.objects.moving_platform import MovingPlatform
from src.entities.objects.fire_bar import FireBar
from src.entities.enemies.goomba import Goomba
from src.entities.enemies.koopa import KoopaGreen
from src.entities.enemies.buzzy_beetle import BuzzyBeetle
from src.entities.enemies.hammer_bro import HammerBro
from src.entities.enemies.piranha_plant import PiranhaPlant
from src.entities.enemies.bullet_bill import BulletBill
from src.entities.enemies.lakitu import Lakitu
from src.entities.enemies.podoboo import Podoboo
from src.entities.enemies.bowser import Bowser
from src.rendering.effects import EffectManager
from src.levels.level_loader import load_level
from src.physics.collision import resolve_collisions_x, resolve_collisions_y

ENEMY_MAP = {
    "goomba": Goomba,
    "koopa_green": KoopaGreen,
    "buzzy_beetle": BuzzyBeetle,
    "hammer_bro": HammerBro,
    "piranha_plant": PiranhaPlant,
    "podoboo": Podoboo,
    "bowser": Bowser,
}


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
        self._lives = INITIAL_LIVES
        self._score = 0
        self._coins = 0
        self._level_file = "test.json"
        self._load_level()

    def load_level_file(self, filename):
        self._level_file = filename

    def _level_path(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base, "levels", "data", self._level_file)

    def _load_level(self):
        path = self._level_path()
        self.level_data = load_level(path)
        self.tile_map = self.level_data.tile_map
        self.player = Player(*self.level_data.player_start)
        self.player.lives = self._lives
        self.player.score = self._score
        self.player.coins = self._coins
        self.camera = Camera(self.tile_map.pixel_width)
        self.block_manager = BlockManager(self.level_data.blocks)
        self.items = []
        self.fireballs = []
        self.shells = []
        self.effects = EffectManager()
        self.time_remaining = self.level_data.time_limit
        self.time_counter = 0

        # Spawn enemies from level data
        self.enemies = []
        for ed in self.level_data.entities:
            etype = ed.get("type", "")
            ex, ey = ed.get("x", 0), ed.get("y", 0)
            cls = ENEMY_MAP.get(etype)
            if cls:
                self.enemies.append(cls(ex, ey))

        # Level objects
        self.pipes = []
        self.flagpole = None
        self.moving_platforms = []
        self.fire_bars = []
        self.bullet_timer = 0

        if self.level_data.flagpole:
            fp = self.level_data.flagpole
            self.flagpole = Flagpole(fp["x"], fp["y"])

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.input.update(events)

            if self.input.just_pressed("pause"):
                if self.status == STATE_PLAYING:
                    self.status = STATE_PAUSED
                    continue
                elif self.status == STATE_PAUSED:
                    self.status = STATE_PLAYING

            if self.status == STATE_PLAYING:
                self._update()
            self._draw()
            pygame.display.flip()
            self.clock.tick(FPS)

    # ── Block hit callback ──
    def _on_hit_block(self, tx, ty):
        result = self.block_manager.hit_block(tx, ty, self.player.form, self.tile_map)
        if not result:
            return
        action, content, bx, by = result
        px, py = bx * TILE_SIZE, by * TILE_SIZE
        if action == "spawn":
            if content == "mushroom":
                self.items.append(Mushroom(px, py, is_1up=False))
            elif content == "fire_flower":
                self.items.append(FireFlower(px, py))
            elif content == "starman":
                self.items.append(Starman(px, py))
            elif content == "coin":
                self.effects.add_coin_effect(px, py - TILE_SIZE)
                self.player.coins += 1
                self.player.score += 200
            elif content == "1up":
                self.items.append(Mushroom(px, py, is_1up=True))
        elif action == "break":
            self.effects.add_brick_debris(px + 4, py + 4)
            self.effects.add_score_popup(px, py, 50)

    # ── Main update ──
    def _update(self):
        # Player
        self.player.update(self.input, self.tile_map,
                           resolve_collisions_x, resolve_collisions_y,
                           self._on_hit_block)
        self.block_manager.update()

        # Fireball
        if (self.input.just_pressed("jump") and self.player.form == FORM_FIRE
                and not self.player.dead and len(self.fireballs) < MAX_FIREBALLS):
            self.fireballs.append(Fireball(
                self.player.x + (8 if self.player.facing_right else -8),
                self.player.y + 8, self.player.facing_right))

        for fb in self.fireballs:
            fb.update(self.tile_map, resolve_collisions_x, resolve_collisions_y)
        self.fireballs = [f for f in self.fireballs if f.alive]

        # Items
        for item in self.items:
            item.update(self.tile_map, resolve_collisions_x, resolve_collisions_y)
            if not item.alive:
                continue
            pr = self.player.get_hitbox()
            if pr.colliderect(item.get_rect()):
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

        # Enemies
        self._update_enemies()

        # Shells
        self._update_shells()

        # Moving platforms
        for mp in self.moving_platforms:
            mp.update()
            if self.player.on_ground:
                pr = self.player.get_hitbox()
                if pr.colliderect(mp.rect):
                    if self.player.get_hitbox().bottom <= mp.rect.top + 4:
                        self.player.x += mp.dx
                        self.player.y += mp.dy

        # Fire bars
        for fb in self.fire_bars:
            fb.update()
            pr = self.player.get_hitbox()
            for seg in fb.get_segments():
                if pr.colliderect(seg) and not self.player.invincible:
                    if self.player.take_damage():
                        break

        # Podoboo
        for e in self.enemies:
            if isinstance(e, Podoboo) and e.alive:
                e.update()
                pr = self.player.get_hitbox()
                er = e.get_rect()
                if er.width > 0 and pr.colliderect(er):
                    if self.player.invincible:
                        e.alive = False
                        self.player.score += e.score_value
                    else:
                        self.player.take_damage()

        # Flagpole
        if self.flagpole and not self.flagpole.triggered:
            pr = self.player.get_hitbox()
            if pr.colliderect(self.flagpole.get_trigger_rect()):
                score = self.flagpole.trigger(self.player.y)
                self.player.score += score
                self.effects.add_score_popup(self.flagpole.x, self.flagpole.y, score)
                self.time_counter = 0

        # Bullet Bill spawner
        self.bullet_timer += 1
        if self.bullet_timer >= 300:
            self.bullet_timer = 0
            cx = self.camera.offset_x
            bx = cx + SCREEN_W + 16
            self.enemies.append(BulletBill(bx, 192))

        # Effects
        self.effects.update()

        # Timer
        self.time_counter += 1
        if self.time_counter >= FPS:
            self.time_counter = 0
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.player.die()

        # Camera
        self.camera.update(self.player.x)

        # Coin lives
        if self.player.coins >= COINS_PER_LIFE:
            self.player.coins -= COINS_PER_LIFE
            self.player.lives += 1

        # Lava check (tile at player feet)
        from src.core.constants import TILE_LAVA
        tx = int(self.player.x + self.player.width // 2) // TILE_SIZE
        ty = int(self.player.y + self.player.height) // TILE_SIZE
        if 0 <= tx < self.tile_map.width and 0 <= ty < self.tile_map.height:
            if self.tile_map.get_tile(tx, ty) == TILE_LAVA:
                self.player.die()

        # Death handling
        if self.player.dead and self.player.death_timer <= 0:
            self._lives = self.player.lives - 1
            self._score = self.player.score
            self._coins = self.player.coins
            if self._lives <= 0:
                self.status = STATE_GAME_OVER
            else:
                self._load_level()

    def _update_enemies(self):
        pr = self.player.get_hitbox()
        for e in self.enemies:
            if not e.alive:
                continue

            if isinstance(e, (PiranhaPlant, Podoboo)):
                continue
            elif isinstance(e, Lakitu):
                e.update(self.camera.offset_x, self.tile_map)
                er = e.get_rect()
                if er.width > 0 and pr.colliderect(er):
                    if self.player.invincible:
                        e.active = False
                        e.respawn_timer = 300
                        self.player.score += e.score_value
                    elif pr.bottom < er.centery and self.player.vy > 0:
                        e.active = False
                        e.respawn_timer = 300
                        self.player.vy = -3.0
                        self.player.score += e.score_value
                continue
            elif isinstance(e, BulletBill):
                e.update(self.camera.offset_x)
            elif isinstance(e, (Goomba, KoopaGreen, BuzzyBeetle, HammerBro)):
                e.update(self.tile_map, resolve_collisions_x, resolve_collisions_y)
            elif isinstance(e, Bowser):
                e.update(self.tile_map)

            # Fireball vs enemy
            for fb in self.fireballs:
                if not fb.alive:
                    continue
                er = e.get_rect()
                if er.width > 0 and fb.get_rect().colliderect(er):
                    score = e.hit_by_fireball()
                    fb.alive = False
                    if score > 0:
                        self.effects.add_score_popup(int(e.x), int(e.y), score)
                        self.player.score += score

            if not e.alive:
                continue

            # Player vs enemy collision
            er = e.get_rect()
            if er.width == 0 or not pr.colliderect(er):
                continue

            # Stomp check
            is_stompable = not isinstance(e, (Bowser,))
            if (is_stompable and not isinstance(e, HammerBro)
                    and pr.bottom < er.centery + 4 and self.player.vy >= 0):
                if self.player.invincible:
                    e.alive = False
                    self.player.score += e.score_value
                    self.effects.add_score_popup(int(e.x), int(e.y), e.score_value)
                    continue
                score = e.stomp()
                self.player.vy = -3.0
                self.player.score += score
                self.effects.add_score_popup(int(e.x), int(e.y), score)

                # Koopa → shell
                if isinstance(e, KoopaGreen):
                    shell = Shell(int(e.x), int(e.y) + 8)
                    self.shells.append(shell)
                elif isinstance(e, BuzzyBeetle):
                    shell = Shell(int(e.x), int(e.y) + 8)
                    self.shells.append(shell)
            elif self.player.invincible:
                e.alive = False
                self.player.score += e.score_value
                self.effects.add_score_popup(int(e.x), int(e.y), e.score_value)
            else:
                self.player.take_damage()

        self.enemies = [e for e in self.enemies if e.alive]

    def _update_shells(self):
        pr = self.player.get_hitbox()
        for shell in self.shells:
            shell.update(self.tile_map,
                         resolve_collisions_x, resolve_collisions_y)
            if not shell.alive:
                continue

            sr = shell.get_rect()
            if not pr.colliderect(sr):
                continue

            if shell.moving:
                shell.vx = 0
                shell.moving = False
                self.effects.add_score_popup(int(shell.x), int(shell.y), 0)
            else:
                dx = 1 if self.player.x > shell.x else -1
                shell.kick(dx)

            # Shell vs enemies
            if shell.moving:
                for e in self.enemies:
                    if not e.alive:
                        continue
                    er = e.get_rect()
                    if er.width > 0 and sr.colliderect(er):
                        if isinstance(e, (Goomba, KoopaGreen, BuzzyBeetle, HammerBro)):
                            e.alive = False
                            score = shell.get_kill_score()
                            self.player.score += score
                            self.effects.add_score_popup(int(e.x), int(e.y), score)
        self.shells = [s for s in self.shells if s.alive]

    # ── Drawing ──
    def _draw(self):
        surf = self.logic_surface
        surf.fill(SKY_BLUE if self.level_data.theme == "overworld" else BLACK)

        if self.status == STATE_GAME_OVER:
            self._draw_game_over(surf)
            scaled = pygame.transform.scale(surf, (WIN_W, WIN_H))
            self.screen.blit(scaled, (0, 0))
            return

        self.tile_map.draw(surf, self.camera.offset_x)

        # Block bounce offsets
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

        for mp in self.moving_platforms:
            mp.draw(surf, self.camera.offset_x)
        for fb in self.fire_bars:
            fb.draw(surf, self.camera.offset_x)
        for p in self.pipes:
            p.draw(surf, self.camera.offset_x)

        for item in self.items:
            item.draw(surf, self.camera.offset_x)
        for fb in self.fireballs:
            fb.draw(surf, self.camera.offset_x)

        for e in self.enemies:
            e.draw(surf, self.camera.offset_x)
        for s in self.shells:
            s.draw(surf, self.camera.offset_x)

        if self.flagpole:
            self.flagpole.draw(surf, self.camera.offset_x)

        self.effects.draw(surf, self.camera.offset_x)
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
        y = 2
        self._draw_text(surf, "MARIO", 8, y)
        self._draw_text(surf, f"{self.player.score:06d}", 8, y + 10)
        self._draw_text(surf, f"x{self.player.coins:02d}", 80, y + 10)
        self._draw_text(surf, "WORLD", 140, y)
        self._draw_text(surf, f"{self.level_data.world}-{self.level_data.level}", 148, y + 10)
        self._draw_text(surf, "TIME", 200, y)
        self._draw_text(surf, f"{self.time_remaining:03d}", 206, y + 10)

    def _draw_text(self, surf, text, x, y):
        surf.blit(self.font.render(text, True, WHITE), (x, y))

    def _draw_game_over(self, surf):
        surf.fill(BLACK)
        text = self.font.render("GAME OVER", True, WHITE)
        surf.blit(text, (SCREEN_W // 2 - text.get_width() // 2, SCREEN_H // 2 - 4))
