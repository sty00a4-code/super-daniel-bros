from settings import *
import pygame as pg
from pygame import *
from tilemap import *
from enum import Enum
from time import time as t
from entities import Entity

class Animation:
    """Animation class consisting of a list of sprites and an animation speed
    """
    def __init__(self, sprites: list[Surface], speed: float = 1):
        self.sprites = sprites
        self.speed = speed
    def cycle(self) -> Surface:
        """Returns the current frame of the animation dependent on the time
        
        Returns:
            Surface: the current frame
        """
        if len(self.sprites) == 1:
            return self.sprites[0]
        return self.sprites[int(t() * self.speed % len(self.sprites))]

# player animations
ANIMATIONS = dict()
ANIMATIONS["idle"] = Animation([pg.image.load("assets/duck/idle.png")])
ANIMATIONS["walk"] = Animation([
    pg.image.load("assets/duck/walk_1.png"),
    pg.image.load("assets/duck/idle.png")
], 10)
ANIMATIONS["jump"] = Animation([pg.image.load("assets/duck/jump.png")])
ANIMATIONS["glide"] = Animation([
    pg.image.load("assets/duck/glide_1.png"),
    pg.image.load("assets/duck/glide_2.png"),
    pg.image.load("assets/duck/glide_3.png"),
    pg.image.load("assets/duck/glide_2.png"),
], 10)
ANIMATIONS["attack"] = Animation([pg.image.load("assets/duck/idle.png")])
ANIMATIONS["throw"] = Animation([pg.image.load("assets/duck/idle.png")])


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
    def start(self, tilemap: TileMap):
        self.rect.x = tilemap.spawn[0] * TILE_SIZE
        self.rect.y = tilemap.spawn[1] * TILE_SIZE
    def update(self, dt: float, tilemap: TileMap, input: Input):
        self.state = State.Idle
        self.air_time += dt
        if self.grounded:
            self.air_time = 0
        acc = 0
        if input.right:
            self.dir = 1
            acc += 1
            self.state = State.Walk
        if input.left:
            self.dir = -1
            acc -= 1
            self.state = State.Walk
        self.vel.x += acc * (PLAYER_SPEED if self.grounded else PLAYER_SPEED / 4)
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
        
        if input.jump and self.vel.y > PLAYER_GLIDE_VEL:
            self.vel.y = PLAYER_GLIDE_VEL
        
        if input.jump:
            if self.air_time < PLAYER_LEAP_TIME:
                self.vel.y = -PLAYER_JUMP
        
        self.rect.x += self.vel.x * dt
        self.rect.y += self.vel.y * dt
        
        self.collide(tilemap)
        self.is_grounded(tilemap)
        if not self.grounded:
            if self.vel.y > 0 and input.jump:
                self.state = State.Glide
            else:
                self.state = State.Jump
    def draw(self, screen: Surface, camera: Vector2, debug = False):
        rect = Rect(self.rect.left - camera.x - TILE_SIZE / 2, self.rect.top - camera.y - TILE_SIZE, self.rect.w, self.rect.h)
        img = transform.flip(ANIMATIONS[self.state.value].cycle(), self.dir == -1, False)
        screen.blit(img, rect)
        if debug:
            draw.rect(screen, Color(255, 255, 255, 255 // 2), self.rect, width=1)