from settings import *
from pygame import *
from player_module.state import State
from player_module.health import Health
from tilemap import *
from entities.entity import Entity
from entities.egg import Egg
from entities.bomb import Bomb
from animation import load_animations
from game_state import GameState

PLAYER_SPEED = 60
PLAYER_FRICTION = 40
PLAYER_MAX_VEL = 310
PLAYER_JUMP = 420
PLAYER_LEAP_TIME = 0.1
PLAYER_GLIDE_VEL = 100
PLAYER_THROW_DELAY = 0.25
PLAYER_DAMAGE_COOLDOWN = 0.5
PLAYER_KNOCKBACK = 500
PLAYER_ATTACK_DELAY = 0.05
PLAYER_ATTACK_OFF_DELAY = 0.15


class Player(Entity):
    """Main player class"""

    def __init__(self, pos: Vector2):
        self.rect = Rect(0, 0, TILE_SIZE, TILE_SIZE)  # Rectangle with position and size
        self.rect.center = (pos.x, pos.y)  # sets the center of the rect
        self.vel = Vector2(0, 0)  # velocity for physics
        self.state = State.Idle  # current state
        self.animations = load_animations("duck")  # animations
        self.grounded = False  # on the a ground or not
        self.air_time = 0  # how long in the air
        self.dir = 1  # facing direction
        self.throw_time = 0  # how long since the last time thrown
        self.charge = 0  # how long the throw button is held
        self.score = dict()
        self.acc = 0
        self.health = Health(3)
        self.damage_timer = 0
        self.upgrades = set()
        self.attack_timer = PLAYER_ATTACK_DELAY

    def start(self, tilemap: TileMap):
        # spawn in tilemap
        self.rect.x = tilemap.spawn[0] * TILE_SIZE
        self.rect.y = tilemap.spawn[1] * TILE_SIZE
        self.vel = Vector2(0, 0)  # velocity for physics
        self.state = State.Idle
        self.animations.play(self.state.value)
        self.air_time = 0  # how long in the air
        self.dir = 1  # facing direction
        self.throw_time = 0  # how long since the last time thrown
        self.charge = 0  # how long the throw button is held
        self.score = dict()
        self.acc = 0
        self.health.reset()
        self.damage_timer = 0
        self.upgrades = set()

    def update(self, dt: float, game):
        if game.state == GameState.Scene:
            if self.grounded:
                if self.vel.x > PLAYER_FRICTION:
                    self.vel.x -= PLAYER_FRICTION
                elif self.vel.x < -PLAYER_FRICTION:
                    self.vel.x += PLAYER_FRICTION
                else:
                    self.vel.x = 0
            return super().update(dt, game)
        last_state = self.state  # remember state
        self.animations.update(dt)

        self.air_time += dt
        self.throw_time += dt
        self.damage_timer += dt
        self.attack_timer += dt

        self.update_ground_state()

        acc = 0
        if self.state == State.Throw:
            self.handle_throw(game, dt)
        elif self.state in [State.Attack1, State.Attack2, State.Attack3]:
            self.handle_attack(game)
            if self.attack_timer >= PLAYER_ATTACK_OFF_DELAY:
                self.state = State.Idle
        elif self.state in [State.Idle, State.Walk]:
            self.handle_walk_and_idle(game)
            self.handle_attack(game)
        elif self.state in [State.Jump, State.Glide]:
            self.handle_throw_glide(game)
            self.handle_jump_and_glide(game)

        # gliding (add "physics")
        if game.input.jump and self.vel.y > PLAYER_GLIDE_VEL:
            self.vel.y = PLAYER_GLIDE_VEL
        # jumping(add "physics")
        if game.input.jump:
            if self.air_time < PLAYER_LEAP_TIME:
                self.vel.y = -PLAYER_JUMP
        # friction(add "physic")
        if acc == 0 and self.grounded:
            if self.vel.x > PLAYER_FRICTION:
                self.vel.x -= PLAYER_FRICTION
            elif self.vel.x < -PLAYER_FRICTION:
                self.vel.x += PLAYER_FRICTION
            else:
                self.vel.x = 0
        # limit velocity
        if self.vel.x > PLAYER_MAX_VEL:
            self.vel.x = PLAYER_MAX_VEL
        elif self.vel.x < -PLAYER_MAX_VEL:
            self.vel.x = -PLAYER_MAX_VEL

        self.vel.y += GRAVITY  # apply gravity
        # update position
        self.rect.x += self.vel.x * dt
        self.rect.y += self.vel.y * dt

        self.check_goal(game)
        self.collide(game)
        self.is_grounded(game)

        # update state of not grounded anymore
        self.update_air_state(game)
        # update to throw state
        self.update_throw_state(game)

        # dead
        if self.rect.bottom > game.tilemap.height * TILE_SIZE - 1:
            self.rect.bottom = game.tilemap.height * TILE_SIZE - 1
            self.state = State.Dead
            game.dead()

        # state changed, reset time
        if last_state != self.state:
            self.animations.play(self.state.value)

    def damage(self, game, entity, damage: int = 1):
        if self.damage_timer >= PLAYER_DAMAGE_COOLDOWN:
            if self.health.damage(damage):
                game.dead()
                self.state = State.Dead
                self.animations.play(self.state.value)
            self.damage_timer = 0
            if entity is not None:
                self.vel.x = (
                    PLAYER_KNOCKBACK
                    if self.rect.centerx > entity.rect.centerx
                    else -PLAYER_KNOCKBACK
                )
            self.vel.y = -PLAYER_KNOCKBACK * 1.5

    def check_goal(self, game):
        (cx, cy) = (self.rect.centerx, self.rect.centery)
        c = game.tilemap.get_rect(cx // TILE_SIZE, cy // TILE_SIZE)
        tile = game.tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
        if tile is Tile:
            tile = tile.tile
        if TILE_DATA[tile].action == "goal":
            if self.rect.colliderect(c):
                game.goal()
        if TILE_DATA[tile].action == "hurt":
            if self.rect.colliderect(c):
                self.damage(game, None)

    def update_ground_state(self):
        if self.grounded:
            # not in air anymore
            self.air_time = 0
            if self.state in [State.Jump, State.Glide]:
                self.state = State.Idle

    def update_air_state(self, game):
        """Handles the player's state when not grounded"""
        if not self.grounded:
            if self.vel.y > 0 and game.input.jump:
                self.state = State.Glide
            else:
                self.state = State.Jump

    def update_throw_state(self, game):
        """Handles transition to throw state"""
        if self.state in [State.Idle, State.Walk, State.Glide] and game.input.throw:
            if self.throw_time > PLAYER_THROW_DELAY:
                self.state = State.Throw if self.state != State.Glide else State.Glide
            else:
                self.charge = 0

    def handle_attack(self, game):
        if game.input.attack:
            if self.state in [State.Idle, State.Walk]:
                self.state = State.Attack1
            elif (
                self.state == State.Attack1 and self.attack_timer >= PLAYER_ATTACK_DELAY
            ):
                self.state = State.Attack2
            elif (
                self.state == State.Attack2 and self.attack_timer >= PLAYER_ATTACK_DELAY
            ):
                self.state = State.Attack3
            elif (
                self.state == State.Attack3 and self.attack_timer >= PLAYER_ATTACK_DELAY
            ):
                self.state = State.Attack1
            self.vel.x = self.dir * PLAYER_SPEED * 20
            self.attack_timer = 0

    def handle_jump_and_glide(self, game):
        # move without changing to walk state
        acc = 0
        if game.input.right:
            self.dir = 1
            acc += 1
        if game.input.left:
            self.dir = -1
            acc -= 1
        self.vel.x += acc * (PLAYER_SPEED if self.grounded else PLAYER_SPEED / 4)

    def handle_walk_and_idle(self, game):
        acc = 0
        if game.input.right:
            self.dir = 1
            acc += 1
            self.state = State.Walk
        elif game.input.left:
            self.dir = -1
            acc -= 1
            self.state = State.Walk
        else:
            self.state = State.Idle

        # apply to velocity
        self.move(acc)

    def move(self, acc: float):
        self.vel.x += acc * (PLAYER_SPEED if self.grounded else PLAYER_SPEED / 4)

    def handle_throw(self, game, dt):
        # face in the direction of the mouse
        if game.input.cursor.x > self.rect.centerx:
            self.dir = 1
        elif game.input.cursor.x < self.rect.centerx:
            self.dir = -1
        self.charge += dt  # build up charge
        if not game.input.throw:  # throw button released
            self.throw_egg(game)
            self.state = State.Idle

    def handle_throw_glide(self, game):
        if (
            game.input.throw
            and self.throw_time > PLAYER_THROW_DELAY
            and self.state == State.Glide
        ):
            self.throw_egg_glide(game)

    def throw_egg(self, game):
        egg = self.egg_factory(game)
        egg.rect.centerx = self.rect.left if self.dir > 0 else self.rect.right
        egg.rect.centery = self.rect.top
        pos = Vector2(self.rect.centerx, self.rect.centery)
        dir = (game.input.cursor - pos).normalize()
        dir.y *= 1.5
        egg.vel += dir * (min(self.charge * 200, 20) + 20) * 25
        game.entities.append(egg)
        self.throw_time = 0
        self.charge = 0

    def throw_egg_glide(self, game):
        egg = self.egg_factory(game)
        egg.rect.centerx = self.rect.left if self.dir > 0 else self.rect.right
        egg.rect.centery = self.rect.centery
        game.entities.append(egg)
        self.throw_time = 0
        self.charge = 0

    def egg_factory(self, game):
        if "bomb" in self.upgrades:
            return Bomb()
        else:
            return Egg()

    def upgrade(self, name: str):
        self.upgrades.add(name)

    def draw(self, game, debug=False):
        rect = Rect(
            self.rect.left - game.camera.x - TILE_SIZE / 2,
            self.rect.top - game.camera.y - TILE_SIZE,
            self.rect.w,
            self.rect.h,
        )
        img = transform.flip(self.animations.sprite(), self.dir == -1, False)
        if game.state != GameState.Game or not (
            self.damage_timer <= PLAYER_DAMAGE_COOLDOWN and bool(t() // 50_000_000 % 2)
        ):
            game.screen.blit(img, rect)
        if debug:
            draw.rect(game.screen, Color(255, 255, 255, 255 // 2), rect, width=1)
