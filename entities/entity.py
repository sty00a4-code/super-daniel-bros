from settings import *
import pygame as pg
from pygame import *
from tilemap import TILE_DATA, Tile


class Entity:
    def __init__(self, rect: Rect):
        self.rect = rect
        self.vel = Vector2(0, 0)
        self.grounded = False
        self.wall_left = False
        self.wall_right = False
        self.dir = 1
        self.transparent = False

    def update(self, dt: float, game):
        self.vel.y += GRAVITY  # apply gravity
        # apply friction
        if self.grounded:
            self.vel.x *= 0.9
        # apply velocity
        self.rect.x += self.vel.x * dt
        self.rect.y += self.vel.y * dt
        self.collide(game)
        self.is_grounded(game)
        self.is_wall_left(game)
        self.is_wall_right(game)

    def is_grounded(self, game):
        self.grounded = False
        (cx, cy) = (self.rect.centerx, self.rect.bottom + 1)
        tile = game.tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
        if tile is Tile:
            tile = tile.tile
        if TILE_DATA[tile].solid:
            self.grounded = True
    def is_wall_left(self, game):
        self.wall_left = False
        (cx, cy) = (self.rect.left - 1, self.rect.centery)
        tile = game.tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
        if tile is Tile:
            tile = tile.tile
        if TILE_DATA[tile].solid:
            self.wall_left = True
    def is_wall_right(self, game):
        self.wall_right = False
        (cx, cy) = (self.rect.right + 1, self.rect.centery)
        tile = game.tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
        if tile is Tile:
            tile = tile.tile
        if TILE_DATA[tile].solid:
            self.wall_right = True

    def damage(self, game, entity):
        pass
    
    def destroy(self, game):
        game.entities.remove(self)

    def collide(self, game):
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel.x = 0
        if self.rect.right > game.tilemap.width * TILE_SIZE:
            self.rect.right = game.tilemap.width * TILE_SIZE
            self.vel.x = 0
        if self.rect.bottom > game.tilemap.height * TILE_SIZE:
            self.rect.bottom = game.tilemap.height * TILE_SIZE
            self.vel.y = 0
        # bottom
        if self.vel.y > 0:
            (cx, cy) = (self.rect.centerx, self.rect.bottom)
            c = game.tilemap.get_rect(cx // TILE_SIZE, cy // TILE_SIZE)
            tile = game.tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
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
            c = game.tilemap.get_rect(cx // TILE_SIZE, cy // TILE_SIZE)
            tile = game.tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
            if tile is Tile:
                tile = tile.tile
            if TILE_DATA[tile].solid:
                if self.rect.colliderect(c):
                    self.rect.top = c.bottom
                    self.vel.y = 0
                    self.air_time = 1
        # left
        if self.vel.x < 0:
            (cx, cy) = (self.rect.left, self.rect.centery)
            c = game.tilemap.get_rect(cx // TILE_SIZE, cy // TILE_SIZE)
            tile = game.tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
            if tile is Tile:
                tile = tile.tile
            if TILE_DATA[tile].solid:
                if self.rect.colliderect(c):
                    self.rect.left = c.right
                    self.vel.x = 0
        # right
        if self.vel.x > 0:
            (cx, cy) = (self.rect.right, self.rect.centery)
            c = game.tilemap.get_rect(cx // TILE_SIZE, cy // TILE_SIZE)
            tile = game.tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
            if tile is Tile:
                tile = tile.tile
            if TILE_DATA[tile].solid:
                if self.rect.colliderect(c):
                    self.rect.right = c.left
                    self.vel.x = 0
        # bottom-left
        if self.vel.y > 0 and self.vel.x < 0:
            (cx, cy) = (self.rect.left, self.rect.bottom)
            c = game.tilemap.get_rect(cx // TILE_SIZE, cy // TILE_SIZE)
            tile = game.tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
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
            c = game.tilemap.get_rect(cx // TILE_SIZE, cy // TILE_SIZE)
            tile = game.tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
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
            c = game.tilemap.get_rect(cx // TILE_SIZE, cy // TILE_SIZE)
            tile = game.tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
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
            c = game.tilemap.get_rect(cx // TILE_SIZE, cy // TILE_SIZE)
            tile = game.tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
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
        rect = Rect(
            self.rect.left - camera.x,
            self.rect.top - camera.y,
            self.rect.w,
            self.rect.h,
        )
        draw.rect(screen, Color(255, 0, 0), rect, width=1)
