from settings import *
from pygame import *
from tilemap import *
from entities.entity import Entity
from animation import load_animations


class Item(Entity):
    def __init__(self, name: str):
        super().__init__(Rect(0, 0, TILE_SIZE, TILE_SIZE))
        self.name = name
        self.animations = load_animations(name)

    def update(self, dt, game):
        if game.player.rect.colliderect(self.rect):
            game.player.upgrade(self.name)
            self.destroy(game)

    def draw(self, screen, camera):
        rect = Rect(
            self.rect.x - camera.x,
            self.rect.y
            - camera.y
            + sin(t() / 200_000_000 + self.rect.x * self.rect.y) * 2,
            self.rect.width,
            self.rect.height,
        )
        screen.blit(self.animations.sprite(), rect)
        # draw.rect(screen, "red", self.rect, 1)

    def damage(self, game, entity):
        print(f"[HIT] {self.__class__} <- {entity.__class__}")
