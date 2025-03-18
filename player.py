from settings import *
import pygame as pg
from pygame import *
from tilemap import *
from enum import Enum
from time import time as t

class Animation:
    def __init__(self, sprites: list[Surface], speed: float = 1):
        self.sprites = sprites
        self.speed = speed
    def cycle(self) -> Surface:
        return self.sprites[int(t() * self.speed % len(self.sprites))]
SPRITES = dict()
SPRITES["idle"] = Animation([pg.image.load("assets/duck/idle.png")])
SPRITES["walk"] = Animation([
    pg.image.load("assets/duck/walk_1.png"),
    pg.image.load("assets/duck/idle.png")
], 10)
SPRITES["jump"] = Animation([pg.image.load("assets/duck/idle.png")])
SPRITES["glide"] = Animation([pg.image.load("assets/duck/idle.png")])
SPRITES["attack"] = Animation([pg.image.load("assets/duck/idle.png")])
SPRITES["throw"] = Animation([pg.image.load("assets/duck/idle.png")])


class State(Enum):
    Idle = "idle"
    Walk = "walk"
    Jump = "jump"
    Glide = "glide"
    Attack = "attack"
    Throw = "throw"

class Input:
    def __init__(self):
        self.left = False
        self.right = False
        self.jump = False
        self.attack = False
        self.throw = False
    def event(self, event: event.Event):
        match event.type:
            case pg.KEYDOWN if event.key == K_a:
                self.left = True
            case pg.KEYUP if event.key == K_a:
                self.left = False
            case pg.KEYDOWN if event.key == K_d:
                self.right = True
            case pg.KEYUP if event.key == K_d:
                self.right = False
            case pg.KEYDOWN if event.key == K_w:
                self.jump = True
            case pg.KEYUP if event.key == K_w:
                self.jump = False
            case pg.KEYDOWN if event.key == K_n:
                self.attack = True
            case pg.KEYUP if event.key == K_n:
                self.attack = False
            case pg.KEYDOWN if event.key == K_m:
                self.throw = True
            case pg.KEYUP if event.key == K_m:
                self.throw = False
class Player:
    def __init__(self, pos: Vector2):
        self.rect = Rect(0, 0, TILE_SIZE, TILE_SIZE)
        self.rect.center = (pos.x, pos.y)
        self.vel = Vector2(0, 0)
        self.state = State.Idle
        self.grounded = False
        self.air_time = 0
        self.dir = 1
    def update(self, dt: float, input: Input, tilemap: TileMap):
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
        self.vel.x += acc * PLAYER_SPEED
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
    def is_grounded(self, tilemap: TileMap):
        self.grounded = False
        (cx, cy) = (self.rect.centerx, self.rect.bottom + 1)
        c = tilemap.get_rect(cx // TILE_SIZE, cy // TILE_SIZE)
        tile = tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
        if tile is Tile:
            tile = tile.tile
        if TILE_DATA[tile].solid:
            self.grounded = True
    def collide(self, tilemap: TileMap):
        self.grounded = False
        # bottom
        (cx, cy) = (self.rect.centerx, self.rect.bottom)
        c = tilemap.get_rect(cx // TILE_SIZE, cy // TILE_SIZE)
        tile = tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
        if tile is Tile:
            tile = tile.tile
        if TILE_DATA[tile].solid:
            if self.rect.colliderect(c):
                self.grounded = True
                self.rect.bottom = c.top
                self.vel.y = 0
        # top
        (cx, cy) = (self.rect.centerx, self.rect.top)
        c = tilemap.get_rect(cx // TILE_SIZE, cy // TILE_SIZE)
        tile = tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
        if tile is Tile:
            tile = tile.tile
        if TILE_DATA[tile].solid:
            if self.rect.colliderect(c):
                self.rect.top = c.bottom
                self.vel.y = 0
                self.air_time = PLAYER_LEAP_TIME
        # left
        (cx, cy) = (self.rect.left, self.rect.centery)
        c = tilemap.get_rect(cx // TILE_SIZE, cy // TILE_SIZE)
        tile = tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
        if tile is Tile:
            tile = tile.tile
        if TILE_DATA[tile].solid:
            if self.rect.colliderect(c):
                self.rect.left = c.right
                self.vel.x = 0
        # right
        (cx, cy) = (self.rect.right, self.rect.centery)
        c = tilemap.get_rect(cx // TILE_SIZE, cy // TILE_SIZE)
        tile = tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
        if tile is Tile:
            tile = tile.tile
        if TILE_DATA[tile].solid:
            if self.rect.colliderect(c):
                self.rect.right = c.left
                self.vel.x = 0
        # bottom-left
        (cx, cy) = (self.rect.left, self.rect.bottom)
        c = tilemap.get_rect(cx // TILE_SIZE, cy // TILE_SIZE)
        tile = tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
        if tile is Tile:
            tile = tile.tile
        if TILE_DATA[tile].solid:
            if self.vel.y > 0:
                if self.rect.colliderect(c):
                    self.rect.bottom = c.top
                    self.vel.y = 0
            else:
                if self.rect.colliderect(c):
                    self.rect.left = c.right
                    self.vel.x = 0
        # bottom-right
        (cx, cy) = (self.rect.right, self.rect.bottom)
        c = tilemap.get_rect(cx // TILE_SIZE, cy // TILE_SIZE)
        tile = tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
        if tile is Tile:
            tile = tile.tile
        if TILE_DATA[tile].solid:
            if self.vel.y > 0:
                if self.rect.colliderect(c):
                    self.rect.bottom = c.top
                    self.vel.y = 0
            else:
                if self.rect.colliderect(c):
                    self.rect.right = c.left
                    self.vel.x = 0
        # top-left
        (cx, cy) = (self.rect.left, self.rect.top)
        c = tilemap.get_rect(cx // TILE_SIZE, cy // TILE_SIZE)
        tile = tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
        if tile is Tile:
            tile = tile.tile
        if TILE_DATA[tile].solid:
            if self.vel.y > 0:
                if self.rect.colliderect(c):
                    self.rect.top = c.bottom
                    self.vel.y = 0
            else:
                if self.rect.colliderect(c):
                    self.rect.left = c.right
                    self.vel.x = 0
        # top-right
        (cx, cy) = (self.rect.right, self.rect.top)
        c = tilemap.get_rect(cx // TILE_SIZE, cy // TILE_SIZE)
        tile = tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
        if tile is Tile:
            tile = tile.tile
        if TILE_DATA[tile].solid:
            if self.vel.y > 0:
                if self.rect.colliderect(c):
                    self.rect.top = c.bottom
                    self.vel.y = 0
            else:
                if self.rect.colliderect(c):
                    self.rect.right = c.left
                    self.vel.x = 0
    def draw(self, screen: Surface, camera: Vector2):
        rect = Rect(self.rect.left - camera.x - TILE_SIZE / 2, self.rect.top - camera.y - TILE_SIZE, self.rect.w, self.rect.h)
        img = transform.flip(SPRITES[self.state.value].cycle(), self.dir == -1, False)
        screen.blit(img, rect)