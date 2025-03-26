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

BARREL_SPEED = 400


class BarrelState(Enum):
    Idle = "idle"


class Barrel(Entity):
    def __init__(self):
        super().__init__(Rect(0, 0, TILE_SIZE, TILE_SIZE))
        self.animations = load_animations("barrel")
        self.dir = -1
        self.state = BarrelState.Idle
        self.body = True

    def update(self, dt, game):
        last_state = self.state
        self.animations.update(dt)
        self.vel.x = self.dir * BARREL_SPEED
        self.collide_bodies(dt, game)
        self.collide_player(dt, game)
        super().update(dt, game)
        if last_state != self.state:
            self.animations.play(self.state.value)

    def collide_bodies(self, dt: float, game):
        for entity in game.entities:
            if entity == self:
                continue
            if entity.__class__ is Egg:
                if self.rect.colliderect(entity.rect):
                    entity.destroy(game)
                    self.destroy(game)
            if entity.body:
                if self.rect.colliderect(entity.rect):
                    entity.damage(game, self)
                    self.destroy(game)

    def collide_player(self, dt: float, game):
        if self.rect.colliderect(game.player.rect):
            if game.player.state not in [
                State.Attack1,
                State.Attack2,
                State.Attack3,
            ]:
                game.player.damage(game, self)
            self.destroy(game)

    def draw(self, screen, camera):
        rect = Rect(
            self.rect.x - camera.x,
            self.rect.y - camera.y,
            self.rect.width,
            self.rect.height,
        )
        img = self.animations.sprite().copy()
        img = transform.flip(img, self.dir == 1, False)
        screen.blit(img, rect)
        draw.rect(screen, "red", rect, 1)
