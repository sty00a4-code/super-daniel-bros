from settings import *
from pygame import *
from tilemap import *
from entities.entity import Entity
from animation import load_animations
from enum import Enum

RAT_SPEED = 200
RAT_SEE_DISTANCE = TILE_SIZE * 6

class RatState(Enum):
    Idle = "idle"
    Walk = "walk"
    Charge = "charge"

class Rat(Entity):
    def __init__(self):
        super().__init__(Rect(0, 0, TILE_SIZE * 2, TILE_SIZE))
        self.animations = load_animations("rat")
        self.dir = -1
        self.state = RatState.Idle
        self.body = True
    def update(self, dt, game):
        last_state = self.state
        self.animations.update(dt)
        if self.wall_left:
            self.dir = 1
        elif self.wall_right:
            self.dir = -1
        distance = Vector2(game.player.rect.centerx, game.player.rect.centery).distance_to((self.rect.centerx, self.rect.centery))
        if self.state == RatState.Idle:
            self.state = RatState.Walk
        elif self.state == RatState.Walk:
            self.vel.x = self.dir * RAT_SPEED * 0.75
        elif self.state == RatState.Charge:
            self.dir = -1 if self.rect.centerx > game.player.rect.centerx else 1
            self.vel.x = self.dir * RAT_SPEED
        if distance < RAT_SEE_DISTANCE:
            self.state = RatState.Charge
        else:
            self.state = RatState.Walk
        self.collide_bodies(dt, game)
        super().update(dt, game)
        if last_state != self.state:
            self.animations.play(self.state.value)
    def collide_bodies(self, dt: float, game):
        for entity in game.entities:
            if entity == self:
                continue
            if entity.body:
                if self.rect.colliderect(entity.rect):
                    self.repell(entity)
        if self.rect.colliderect(game.player.rect):
            self.repell(game.player)
    def repell(self, entity: Entity):
        pos1 = Vector2(self.rect.centerx, self.rect.centery)
        pos2 = Vector2(entity.rect.centerx, entity.rect.centery)
        force = (pos2 - pos1).x
        if self.state != RatState.Charge:
            if force > 0:
                self.dir = -1
            elif force < 0:
                self.dir = 1
        self.vel.x = (self.rect.w / 2 + entity.rect.w / 2 - force) * 3
    def draw(self, screen, camera):
        rect = Rect(
            self.rect.x - camera.x,
            self.rect.y - camera.y - TILE_SIZE,
            self.rect.width,
            self.rect.height,
        )
        img = self.animations.sprite().copy()
        img = transform.flip(img, self.dir == 1, False)
        screen.blit(img, rect)
        # draw.rect(screen, "red", self.rect, 1)
    def damage(self, game, entity):
        print(f"[HIT] {self.__class__} <- {entity.__class__}")