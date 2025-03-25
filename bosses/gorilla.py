from bosses.boss import Boss
from enum import Enum
from animation import load_animations
from player_module.health import Health
from game_state import GameState
from pygame import *


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
    Smash = "smash"
    Stunned = "stunned"
    Challenge = "challenge"
    Wait = "wait"
    Jump = "jump"
    Pos1 = "pos1"
    Pos2 = "pos2"
    Pos3 = "pos3"


GORILLA_SPEED = 60
GORILLA_IDLE_TIME = 3
GORILLA_JUMP_TIME = 3
GORILLA_SMASH_TIME = 5
GORILLA_BARREL_TIME = 3
GORILLA_BARREL_WAIT_TIME = 2
GORILLA_STUNNED_TIME = 3
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
        self.animations = load_animations("gorilla")

    def update(self, dt, game):
        if game.state == GameState.Scene:
            return super().update(dt, game)
        last_state = self.state
        self.animations.update(dt)

        self.state_timer += dt

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

    def draw(self, screen, camera):
        rect = Rect(
            self.rect.x - camera.x - 10, self.rect.y - camera.y - 32, self.rect.w, self.rect.h
        )
        img = self.animations.sprite()
        screen.blit(img, rect)
        super().draw(screen, camera)

    def handle_stunned(self, dt, game):
        if self.state_timer < GORILLA_STUNNED_TIME:
            self.state = GorillaState.Stunned
        else:
            self.state = GorillaState.Idle

    def handle_barrel(self, dt, game):
        if self.barrels < 3:
            if self.state_timer < GORILLA_BARREL_TIME:
                self.state = GorillaState.HoldBarrel
            elif self.state_timer < GORILLA_BARREL_TIME + GORILLA_BARREL_WAIT_TIME:
                self.throw_barrel(dt, game)
                self.barrels += 1
                self.state_timer = 0
        else:
            self.state = GorillaState.Idle

    def handle_jump(self, dt, game):
        if self.state_timer < GORILLA_JUMP_TIME:
            self.state = GorillaState.Idle
        else:
            self.state = GorillaState.Jump
            self.jump(dt, game)

    def handle_smash(self, dt, game):
        if self.state_timer < GORILLA_SMASH_TIME:
            self.state = GorillaState.Smash
        else:
            self.state = GorillaState.Idle

    def next_state(self):
        if self.boss_state in [GorillaBossState.Idle, GorillaBossState.Stunned]:
            self.boss_state = GORILLA_STATES[self.boss_state_index % 3]
            if self.boss_state == GorillaBossState.Barrel:
                self.barrels = 0
            self.state_timer = 0
            self.boss_state_index += 1
        else:
            self.boss_state_index += 1
            self.state_timer = 0
            self.boss_state = GorillaBossState.Idle

    def throw_barrel(self, dt, game):
        pass

    def jump(self, dt, game):
        pass
