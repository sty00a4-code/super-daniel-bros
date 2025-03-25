from bosses.boss import Boss
from enum import Enum
from animation import load_animations
from player_module.health import Health


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
    Jump = "Jump"


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
        self.health = Health(20)
        self.boss_state = GorillaBossState.Idle
        self.state = GorillaState.Idle
        self.boss_state_index = 0
        self.state_timer = 0
        self.barrels = 0
        self.animations = load_animations("gorilla")

    def update(self, dt, game):
        last_state = self.state

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

        if last_state != self.state:
            self.animations.play(self.state.value)

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
