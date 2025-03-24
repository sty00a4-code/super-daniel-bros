from settings import *
from pygame import *
from tilemap import *
from entities.entity import Entity
from entities.explosion import Explosion

EGG_IMG = image.load("assets/tiles/egg.png")


class Egg(Entity):
    def __init__(self):
        super().__init__(Rect(0, 0, TILE_SIZE / 2, TILE_SIZE / 2))
        self.hit = False

    def update(self, dt, game):
        super().update(dt, game)
        for entity in game.entities:
            if entity == self:
                continue
            if entity.rect.colliderect(self.rect) and not entity.transparent:
                entity.damage(game, self)
                self.hit = True
        # delete if hit something
        if self.hit:
            self.destroy(game)

    def collide(self, game):
        (cx, cy) = (self.rect.centerx, self.rect.centery)
        c = game.tilemap.get_rect(cx // TILE_SIZE, cy // TILE_SIZE)
        tile = game.tilemap.get(cx // TILE_SIZE, cy // TILE_SIZE)
        if tile is Tile:
            tile = tile.tile
        if TILE_DATA[tile].solid:
            if self.rect.colliderect(c):
                self.hit = True

    def draw(self, screen, camera):
        rect = Rect(
            self.rect.x - TILE_SIZE / 4 - camera.x,
            self.rect.y - TILE_SIZE / 4 - camera.y,
            TILE_SIZE,
            TILE_SIZE,
        )
        screen.blit(EGG_IMG, rect)
        # draw.rect(screen, "red", self.rect, 1)
