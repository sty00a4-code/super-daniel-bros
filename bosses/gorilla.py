from bosses.boss import Boss
from enum import Enum
from animation import load_animations
from player_module.health import Health
from player_module.state import PLAYER_ATTACK_STATES
from game_state import GameState
from pygame import *
from time import time_ns as t
from entities.barrel import Barrel
from entities.egg import Egg


class GorillaBossState(Enum):
    Idle = "idle"  # walks back and forth
    Barrel = "barrel"  # throws barrels, 3
    Jump = "jump"  # jump attack
    Smash = "smash"  # smashes the ground
    Stunned = "stunned"


class GorillaState(Enum):
    Idle = "idle"
    Walk = "walk"
    HoldBarrel = "hold_barrel"
    ThrowBarrel = "throw_barrel"
    Smash = "smash"
    Stunned = "stunned"
    Challenge = "challenge"
    Wait = "wait"
    Jump = "jump"
    Slam = "slam"
    Pos1 = "pos1"
    Pos2 = "pos2"
    Pos3 = "pos3"


GORILLA_SPEED = 60
GORILLA_IDLE_TIME = 3
GORILLA_JUMP_TIME = 2
GORILLA_SMASH_TIME = 5
GORILLA_BARREL_TIME = 0.5
GORILLA_BARREL_WAIT_TIME = 0.5
GORILLA_STUNNED_TIME = 3
GORILLA_DAMAGE_COOLDOWN = 0.5
GORILLA_SLAM_TIME = 1
GORILLA_STATES = [
    GorillaBossState.Barrel,
    GorillaBossState.Jump,
    GorillaBossState.Smash,
]


class Gorilla(Boss):
    def __init__(self):
        super().__init__()
        self.rect = Rect(0, 0, 64 - 20, 32)
        self.health = Health(20)
        self.boss_state = GorillaBossState.Idle
        self.state = GorillaState.Idle
        self.boss_state_index = 0
        self.state_timer = 0
        self.barrels = 0
        self.damage_timer = 0
        self.damage_counter = 0
        self.animations = load_animations("gorilla")

    def update(self, dt, game):
        if game.state == GameState.Scene:
            return super().update(dt, game)
        last_state = self.state
        self.animations.update(dt)

        self.state_timer += dt
        self.damage_timer += dt

        self.handle_damage(dt, game)
        if self.health.health <= 0:
            raise Exception("TODO: Death")

        # print(self.boss_state.value, self.state.value)
        if self.boss_state == GorillaBossState.Idle:
            self.next_state()
        elif self.boss_state == GorillaBossState.Stunned:
            self.handle_stunned(dt, game)
        elif self.boss_state == GorillaBossState.Barrel:
            self.handle_barrel(dt, game)
        elif self.boss_state == GorillaBossState.Jump:
            self.handle_jump(dt, game)
        elif self.boss_state == GorillaBossState.Smash:
            self.handle_smash(dt, game)

        super().update(dt, game)
        if last_state != self.state:
            self.animations.play(self.state.value)

    def move(self, acc: float):
        self.vel.x += acc * GORILLA_SPEED

    def handle_damage(self, dt: float, game):
        if self.state == GorillaState.Stunned:
            if game.player.rect.colliderect(self.rect):
                if (
                    game.player.state in PLAYER_ATTACK_STATES
                    and self.damage_timer >= GORILLA_DAMAGE_COOLDOWN
                ):
                    self.health.damage()
                    self.damage_timer = 0
                    self.damage_counter += 1
                    if self.damage_counter == 3:
                        self.boss_state_index = 2
                        self.state = GorillaState.Idle

    def draw(self, game):
        rect = Rect(
            self.rect.x - game.camera.x - 10,
            self.rect.y - game.camera.y - 32,
            self.rect.w,
            self.rect.h,
        )
        img = transform.flip(self.animations.sprite(), self.dir == -1, False)
        if game.state != GameState.Game or not (
            self.damage_timer <= GORILLA_DAMAGE_COOLDOWN and bool(t() // 50_000_000 % 2)
        ):
            game.screen.blit(img, rect)

    def handle_stunned(self, dt, game):
        if self.state_timer < GORILLA_STUNNED_TIME:
            self.state = GorillaState.Stunned
        else:
            self.boss_state = GorillaBossState.Idle

    def handle_barrel(self, dt, game):
        if self.barrels < 3 or self.state == GorillaState.ThrowBarrel:
            if self.rect.colliderect(game.player.rect):
                game.player.damage(game, self)
            if self.state in [GorillaState.Idle, GorillaState.HoldBarrel]:
                self.dir = 1 if game.player.rect.centerx < self.rect.centerx else -1
                if self.state_timer < GORILLA_BARREL_TIME:
                    self.state = GorillaState.HoldBarrel
                else:
                    self.throw_barrel(dt, game)
                    self.state_timer = 0
            elif self.state == GorillaState.ThrowBarrel:
                if self.state_timer < GORILLA_BARREL_TIME:
                    self.state = GorillaState.ThrowBarrel
                else:
                    self.state = GorillaState.HoldBarrel
                    self.state_timer = 0
        else:
            self.boss_state = GorillaBossState.Idle

    def handle_jump(self, dt, game):
        if self.state_timer < GORILLA_JUMP_TIME and self.state != GorillaState.Slam:
            self.dir = 1 if game.player.rect.centerx < self.rect.centerx else -1
            self.state = GorillaState.Pos1
        elif self.state == GorillaState.Pos1:
            self.state = GorillaState.Jump
            self.jump(dt, game)
        elif self.state == GorillaState.Jump:
            for entity in game.entities:
                if entity.__class__ is Egg:
                    if entity.rect.colliderect(self.rect):
                        self.stun()
            if self.grounded:
                self.state = GorillaState.Slam
                self.state_timer = 0
        elif self.state == GorillaState.Slam:
            if self.state_timer >= GORILLA_SLAM_TIME:
                self.next_state()
            else:
                if self.rect.colliderect(game.player.rect):
                    game.player.damage(game, self)
                self.state = GorillaState.Slam

    def handle_smash(self, dt, game):
        self.dir = 1 if game.player.rect.centerx < self.rect.centerx else -1
        if self.state_timer < GORILLA_SMASH_TIME:
            self.state = GorillaState.Smash
            if self.rect.colliderect(game.player.rect):
                game.player.damage(game, self)
        else:
            self.boss_state = GorillaBossState.Idle

    def next_state(self):
        if self.boss_state in [GorillaBossState.Idle, GorillaBossState.Stunned]:
            self.boss_state = GORILLA_STATES[self.boss_state_index % 3]
            if self.boss_state == GorillaBossState.Barrel:
                self.barrels = 0
                self.state = GorillaState.HoldBarrel
            elif self.boss_state == GorillaBossState.Jump:
                self.state = GorillaState.Pos1
            elif self.boss_state == GorillaBossState.Smash:
                self.state = GorillaState.Smash
            self.state_timer = 0
            self.boss_state_index += 1
            print(f"[STATE] {self.boss_state} {self.boss_state_index}")
        else:
            self.state_timer = 0
            self.boss_state = GorillaBossState.Idle
            print(f"[STATE] {self.boss_state} {self.boss_state_index}")

    def throw_barrel(self, dt, game):
        self.state = GorillaState.ThrowBarrel
        self.barrels += 1
        barrel = Barrel()
        barrel.rect.centerx = self.rect.right if self.dir == -1 else self.rect.left
        barrel.rect.centery = self.rect.centery
        barrel.dir = -self.dir
        game.spawn_entity(barrel)

    def jump(self, dt, game):
        self.move(((game.player.rect.centerx - self.rect.centerx) / 30))
        self.vel.y = -1500
    
    def stun(self):
        self.boss_state = GorillaBossState.Stunned
        self.state_timer = 0
        self.state = GorillaState.Stunned
