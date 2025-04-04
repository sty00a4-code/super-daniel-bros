from settings import *
from pygame import *
from tilemap import *
from entities.entity import Entity
from animation import load_animations


class Collectible(Entity):
    def __init__(self, name: str):
        super().__init__(Rect(0, 0, TILE_SIZE, TILE_SIZE))
        self.name = name
        self.animations = load_animations(name)
        self.transparent = True

    def update(self, dt, game):
        if game.player.rect.colliderect(self.rect):
            if self.name in game.player.score:
                game.player.score[key] += COLLECTIBLES[self.name]
            else:
                game.player.score[key] = COLLECTIBLES[self.name]
            game.player.health.heal()
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
