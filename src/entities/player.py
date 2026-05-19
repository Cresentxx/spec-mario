import pygame
from src.physics.physics import PhysicsBody
from src.core.constants import (
    SMALL_W, SMALL_H, BIG_W, BIG_H,
    WALK_MAX, RUN_MAX, ACCEL, DECEL,
    JUMP_VEL, JUMP_CUT, GRAVITY, MAX_FALL,
    FORM_SMALL, FORM_SUPER, FORM_FIRE,
    MARIO_RED, MARIO_BROWN, WHITE, BLACK,
    INVINCIBLE_FRAMES,
)


class Player(PhysicsBody):
    def __init__(self, x, y):
        super().__init__(x, y, SMALL_W, SMALL_H)
        self.form = FORM_SMALL
        self.facing_right = True
        self.jump_held = False
        self.invincible = False
        self.invincible_timer = 0
        self.dead = False
        self.death_timer = 0
        self.score = 0
        self.coins = 0

    def set_form(self, form):
        old_form = self.form
        self.form = form
        if form == FORM_SMALL:
            self.width = SMALL_W
            self.height = SMALL_H
        else:
            self.width = BIG_W
            self.height = BIG_H
        if old_form == FORM_SMALL and form != FORM_SMALL:
            self.y -= (BIG_H - SMALL_H)

    def update(self, input_handler, tile_map, collision_resolve_x, collision_resolve_y, hit_block_cb):
        if self.dead:
            self.death_timer -= 1
            if self.death_timer > 30:
                self.vy = -3.0
            else:
                self.vy += GRAVITY
            self.y += self.vy
            return

        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

        # Horizontal movement
        max_speed = RUN_MAX if input_handler.is_held("run") else WALK_MAX
        moving = False
        if input_handler.is_held("left"):
            self.vx -= ACCEL
            self.facing_right = False
            moving = True
        if input_handler.is_held("right"):
            self.vx += ACCEL
            self.facing_right = True
            moving = True

        if not moving:
            if abs(self.vx) < DECEL:
                self.vx = 0
            elif self.vx > 0:
                self.vx -= DECEL
            else:
                self.vx += DECEL

        self.vx = max(-max_speed, min(max_speed, self.vx))

        # Jump — 按下立刻起跳
        if input_handler.just_pressed("jump") and self.on_ground:
            self.vy = JUMP_VEL
            self.jump_held = True
            self.on_ground = False

        # Gravity — 按住跳跃键时重力减半实现可变高度
        if self.jump_held and self.vy < 0:
            self.vy += GRAVITY * 0.5
        else:
            self.vy += GRAVITY
        if self.vy > MAX_FALL:
            self.vy = MAX_FALL

        # 松键截断上升速度 → 最低跳
        if input_handler.just_released("jump"):
            self.jump_held = False
            if self.vy < 0:
                self.vy *= JUMP_CUT

        # Move X then resolve
        self.x += self.vx
        collision_resolve_x(self, tile_map)

        # Move Y then resolve
        self.y += self.vy
        collision_resolve_y(self, tile_map, hit_block_cb)

        # Fall off map
        if self.y > 240:
            self.die()

    def die(self):
        if self.dead:
            return
        self.dead = True
        self.vy = -5.0
        self.death_timer = 60
        self.vx = 0

    def take_damage(self):
        if self.invincible:
            return False
        if self.form == FORM_FIRE:
            self.set_form(FORM_SUPER)
            return True
        elif self.form == FORM_SUPER:
            self.set_form(FORM_SMALL)
            return True
        else:
            self.die()
            return True

    def get_hitbox(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, surface, camera_x):
        if self.dead:
            if self.death_timer > 0:
                self._draw_sprite(surface, camera_x, death=True)
            return

        if self.invincible and (self.invincible_timer // 3) % 2 == 0:
            return

        self._draw_sprite(surface, camera_x)

    def _draw_sprite(self, surface, camera_x, death=False):
        x = int(self.x) - camera_x - (self.width - 12) // 2
        y = int(self.y)

        if self.form == FORM_SMALL:
            # Head
            head_color = MARIO_BROWN
            pygame.draw.rect(surface, head_color, (x + 2, y, 10, 6))
            # Face
            face_color = (255, 200, 150)
            pygame.draw.rect(surface, face_color, (x + 3, y + 2, 8, 4))
            # Hat
            hat_color = MARIO_RED
            pygame.draw.rect(surface, hat_color, (x + 1, y - 2, 12, 3))
            # Body
            pygame.draw.rect(surface, MARIO_RED, (x + 2, y + 6, 10, 6))
            # Legs
            leg_color = MARIO_BROWN if not self.facing_right else MARIO_BROWN
            pygame.draw.rect(surface, leg_color, (x + 2, y + 12, 4, 4))
            pygame.draw.rect(surface, leg_color, (x + 8, y + 12, 4, 4))
        else:
            body_color = WHITE if self.form == FORM_FIRE else MARIO_RED
            # Head
            pygame.draw.rect(surface, MARIO_BROWN, (x + 2, y, 10, 8))
            pygame.draw.rect(surface, (255, 200, 150), (x + 3, y + 2, 8, 6))
            # Hat
            pygame.draw.rect(surface, MARIO_RED, (x, y - 2, 14, 3))
            # Body
            pygame.draw.rect(surface, body_color, (x + 1, y + 8, 12, 14))
            # Belt
            pygame.draw.rect(surface, MARIO_BROWN, (x + 2, y + 18, 10, 2))
            # Legs
            pygame.draw.rect(surface, MARIO_BROWN, (x + 1, y + 22, 5, 10))
            pygame.draw.rect(surface, MARIO_BROWN, (x + 8, y + 22, 5, 10))

        if death:
            # X eyes
            cx, cy = x + 7, y + 4
            pygame.draw.line(surface, BLACK, (cx-2, cy-2), (cx+2, cy+2))
            pygame.draw.line(surface, BLACK, (cx+2, cy-2), (cx-2, cy+2))
