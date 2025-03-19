from settings import *
import pygame as pg
from pygame import *
from tilemap import *

class Entity:
    def __init__(self, rect: Rect):
        self.rect = rect
        self.vel = Vector2(0, 0)
        self.grounded = False
        self.dir = 1
    def update(self, dt: float, tilemap: TileMap, entities: list, player):
        self.vel.y += GRAVITY
        if self.grounded:
            self.vel.x *= 0.9
        self.rect.x += self.vel.x * dt
        self.rect.y += self.vel.y * dt
        self.collide(tilemap)
        self.is_grounded(tilemap)
    def is_grounded(self, tilemap: TileMap):
        self.grounded = False
        (cx, cy) = (self.rect.centerx, self.rect.bottom + 1)
        tile = tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
        if tile is Tile:
            tile = tile.tile
        if TILE_DATA[tile].solid:
            self.grounded = True
    def collide(self, tilemap: TileMap):
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel.x = 0
        if self.rect.right > tilemap.width * TILE_SIZE:
            self.rect.right = tilemap.width * TILE_SIZE
            self.vel.x = 0
        if self.rect.bottom > tilemap.height * TILE_SIZE:
            self.rect.bottom = tilemap.height * TILE_SIZE
            self.vel.y = 0
        # bottom
        if self.vel.y > 0:
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
        if self.vel.y < 0:
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
        if self.vel.x < 0:
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
        if self.vel.x > 0:
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
        if self.vel.y > 0 and self.vel.x < 0:
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
        if self.vel.y > 0 and self.vel.x > 0:
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
        if self.vel.y < 0 and self.vel.x < 0:
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
        if self.vel.y < 0 and self.vel.x > 0:
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
        draw.rect(screen, Color(255, 0, 0), self.rect, width=1)