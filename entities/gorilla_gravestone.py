from settings import *
from pygame import *
from tilemap import *
from entities.entity import Entity
from animation import load_animations
from enum import Enum
from player_module.state import State
from player_module.player import Player
from player_module.health import Health
from entities.egg import Egg


class Gravestone(Entity):
    def __init__(self):
        super().__init__(Rect(0, 0, TILE_SIZE * 4, TILE_SIZE * 4))
        self.animations = load_animations("gravestone")
        self.animations.play("idle")

    def update(self, dt, game):
        self.animations.update(dt)
        if self.rect.left <= 0:
            self.destroy(game)
        if self.rect.right >= game.tilemap.width * TILE_SIZE:
            self.destroy(game)
        if self.rect.bottom >= game.tilemap.height * TILE_SIZE:
            self.destroy(game)
        super().update(dt, game)

    def draw(self, screen, camera):
        rect = Rect(
            self.rect.x - camera.x,
            self.rect.y - camera.y - 32,
            self.rect.width,
            self.rect.height,
        )
        screen.blit(self.animations.sprite(), rect)
        # draw.rect(screen, "red", self.rect)
