from pygame import *
from settings import *
from entities.persistent_entities import Persistent_entities

class Explosion(Persistent_entities):

    def __init__(self, game, rect: Rect, lifespan: float = 200, update_after_ticks: int = -1):
        super().__init__(game, Rect(0, 0, TILE_SIZE / 2, TILE_SIZE / 2), lifespan, update_after_ticks) #Rect_Size is Hitbox_Size
        self.rect = rect

    def update(self, dt: float, game):
        super().update(dt, game)

    def draw(self, screen, camera):
        rect = Rect(
            self.rect.x - TILE_SIZE / 4 - camera.x,
            self.rect.y - TILE_SIZE / 4 - camera.y,
            TILE_SIZE,
            TILE_SIZE,
        )
        #screen.blit(self.test, (rect.x, rect.y))
        draw.rect(screen, "red", rect, 1)