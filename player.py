from settings import *
import pygame as pg
from pygame import *
from tilemap import *
from enum import Enum
from time import time as t
from entities import Entity
from egg import *

class Animation:
    """Animation class consisting of a list of sprites and an animation speed
    """
    def __init__(self, sprites: list[Surface], speed: float = 1):
        self.sprites = sprites
        self.speed = speed
        self.time = 0
    def cycle(self, dt) -> Surface:
        self.time += dt
        """Returns the current frame of the animation dependent on the time
        
        Returns:
            Surface: the current frame
        """
        if len(self.sprites) == 1:
            return self.sprites[0]
        return self.sprites[int(self.time * self.speed % len(self.sprites))]

# player animations
ANIMATIONS = dict()
ANIMATIONS["idle"] = Animation([pg.image.load("assets/duck/idle.png")])
ANIMATIONS["walk"] = Animation([
    pg.image.load("assets/duck/walk_1.png"),
    pg.image.load("assets/duck/idle.png")
], 20)
ANIMATIONS["jump"] = Animation([pg.image.load("assets/duck/jump.png")])
ANIMATIONS["glide"] = Animation([
    pg.image.load("assets/duck/glide_1.png"),
    pg.image.load("assets/duck/glide_2.png"),
    pg.image.load("assets/duck/glide_3.png"),
    pg.image.load("assets/duck/glide_2.png"),
], 20)
ANIMATIONS["attack"] = Animation([pg.image.load("assets/duck/idle.png")])
ANIMATIONS["throw"] = Animation([pg.image.load("assets/duck/throw.png")])


class State(Enum):
    Idle = "idle"
    Walk = "walk"
    Jump = "jump"
    Glide = "glide"
    Attack = "attack"
    Throw = "throw"

class Input:
    """Input manager
    
    - left: K_a
    - right: K_d
    - jump: K_w
    - attack: K_n
    - throw: K_m
    """
    def __init__(self):
        self.left = False
        self.right = False
        self.jump = False
        self.attack = False
        self.throw = False
        self.cursor = Vector2(0, 0)
    def mouse(self, camera: Vector2):
        mouse_pos = mouse.get_pos()
        self.cursor.x = mouse_pos[0] / 2 - camera.x
        self.cursor.y = mouse_pos[1] / 2 - camera.y
    def event(self, event: event.Event):
        if event.type in [KEYDOWN, KEYUP]:
            if event.key == K_a:
                self.left = event.type == KEYDOWN
            elif event.key == K_d:
                self.right = event.type == KEYDOWN
            elif event.key == K_w:
                self.jump = event.type == KEYDOWN
            elif event.key == K_SPACE:
                self.throw = event.type == KEYDOWN
class Player(Entity):
    """Main player class
    """
    def __init__(self, pos: Vector2):
        # also has position
        self.rect = Rect(0, 0, TILE_SIZE, TILE_SIZE)
        self.rect.center = (pos.x, pos.y)
        self.vel = Vector2(0, 0)
        self.state = State.Idle
        self.grounded = False
        self.air_time = 0
        self.dir = 1
        self.throw_time = 0
        self.charge = 0
        self.score =  dict()
    def start(self, tilemap: TileMap):
        self.rect.x = tilemap.spawn[0] * TILE_SIZE
        self.rect.y = tilemap.spawn[1] * TILE_SIZE
    def update(self, dt, game):
        self.air_time += dt
        self.throw_time += dt
        current_tile_pos = game.tilemap.real_to_tile(self.rect.center[0], self.rect.center[1])
        current_tile = game.tilemap.get(current_tile_pos[0], current_tile_pos[1])
        if self.grounded:
            self.air_time = 0
            if self.state in [State.Jump, State.Glide]:
                self.state = State.Idle
        acc = 0
        if self.state == State.Throw:
            if game.input.cursor.x > self.rect.centerx:
                self.dir = 1
            elif game.input.cursor.x < self.rect.centerx:
                self.dir = -1
            self.charge += dt
            if not game.input.throw:
                self.throw_egg(game)
                self.state = State.Idle
            if game.input.right:
                self.dir = 1
            if game.input.left:
                self.dir = -1
        elif self.state in [State.Idle, State.Walk]:
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
            self.vel.x += acc * (PLAYER_SPEED if self.grounded else PLAYER_SPEED / 4)
        elif self.state in [State.Jump, State.Glide]:
            if game.input.right:
                self.dir = 1
                acc += 1
            if game.input.left:
                self.dir = -1
                acc -= 1
            self.vel.x += acc * (PLAYER_SPEED if self.grounded else PLAYER_SPEED / 4)
        
        if game.input.jump and self.vel.y > PLAYER_GLIDE_VEL:
            self.vel.y = PLAYER_GLIDE_VEL
        if game.input.jump:
            if self.air_time < PLAYER_LEAP_TIME:
                self.vel.y = -PLAYER_JUMP
        if acc == 0 and self.grounded:
            if self.vel.x > PLAYER_FRICTION:
                self.vel.x -= PLAYER_FRICTION
            elif self.vel.x < -PLAYER_FRICTION:
                self.vel.x += PLAYER_FRICTION
            else:
                self.vel.x = 0
        if self.vel.x > PLAYER_MAX_VEL:
            self.vel.x = PLAYER_MAX_VEL
        elif self.vel.x < -PLAYER_MAX_VEL:
            self.vel.x = -PLAYER_MAX_VEL
        
        self.vel.y += GRAVITY
        self.rect.x += self.vel.x * dt
        self.rect.y += self.vel.y * dt
        
        self.collide(game)
        self.is_grounded(game)
        if not self.grounded:
            if self.vel.y > 0 and game.input.jump:
                self.state = State.Glide
            else:
                self.state = State.Jump
                
        if self.state in [State.Idle, State.Walk] and game.input.throw:
            if self.throw_time > PLAYER_THROW_DELAY:
                self.state = State.Throw
            else:
                self.charge = 0
        if TILE_DATA[current_tile].collectible and TILE_DATA[current_tile].item:
            key = TILE_DATA[current_tile].item
            if key in self.score:
                self.score[key] += 1
            else:
                self.score[key] =  1
            game.tilemap.set(current_tile_pos[0], current_tile_pos[1], 0) 
    def throw_egg(self, game):
        egg = Egg()
        egg.rect.centerx = self.rect.left if self.dir > 0 else self.rect.right
        egg.rect.centery = self.rect.top
        pos = Vector2(self.rect.centerx, self.rect.centery)
        dir = (game.input.cursor - pos).normalize()
        dir.y *= 1.5
        egg.vel += dir * (min(self.charge * 200, 20) + 20) * 25
        game.entities.append(egg)
        self.throw_time = 0
        self.charge = 0
    def draw(self, screen: Surface, camera: Vector2, dt: float, debug = False):
        rect = Rect(self.rect.left - camera.x - TILE_SIZE / 2, self.rect.top - camera.y - TILE_SIZE, self.rect.w, self.rect.h)
        img = transform.flip(ANIMATIONS[self.state.value].cycle(dt), self.dir == -1, False)
        screen.blit(img, rect)
        if debug:
            draw.rect(screen, Color(255, 255, 255, 255 // 2), rect, width=1)