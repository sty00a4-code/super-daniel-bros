from settings import *
from pygame import *
from tilemap import *
from entities.egg import Egg
from entities.explosion import Explosion

BOMB_IMG = image.load("assets/tiles/bomb.png")


class Bomb(Egg):
    def __init__(self):
        super().__init__()

    def destroy(self, game):
        explosion = Explosion(self.rect)
        game.entities.append(explosion)
        super().destroy(game)

    def draw(self, screen, camera):
        rect = Rect(
            self.rect.x - TILE_SIZE / 4 - camera.x,
            self.rect.y - TILE_SIZE / 4 - camera.y,
            TILE_SIZE,
            TILE_SIZE,
        )
        screen.blit(BOMB_IMG, rect)
        # draw.rect(screen, "red", self.rect, 1)
