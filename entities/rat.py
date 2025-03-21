from settings import *
from pygame import *
from tilemap import *
from entities.entity import Entity
from animation import load_animations

class Rat(Entity):
    def __init__(self):
        super().__init__(Rect(0, 0, TILE_SIZE * 2, TILE_SIZE))
        self.animations = load_animations("rat")
    def draw(self, screen, camera):
        rect = Rect(
            self.rect.x - camera.x,
            self.rect.y - camera.y,
            self.rect.width,
            self.rect.height,
        )
        screen.blit(self.animations.sprite(), rect)
        # draw.rect(screen, "red", self.rect, 1)
    def damage(self, game, entity):
        print(f"[HIT] {self.__class__} <- {entity.__class__}")