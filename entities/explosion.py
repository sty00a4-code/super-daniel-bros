from pygame import *
from settings import *
from entities.entity import Entity

class Explosion(Entity):

    def __init__(self, game, rect):
        super().__init__(Rect(0, 0, TILE_SIZE / 2, TILE_SIZE / 2))
        self.rect = rect
        self.timer = 0.2

    
    def update(self, dt: float, game):
        #super().update(dt, game)
        print(self.timer)
        self.timer -= dt
        if self.timer <= 0:
            self.destroy(game)

        

    def draw(self, screen, camera):
        rect = Rect(
            self.rect.x - TILE_SIZE / 4 - camera.x,
            self.rect.y - TILE_SIZE / 4 - camera.y,
            TILE_SIZE,
            TILE_SIZE,
        )
        #screen.blit(self.test, (rect.x, rect.y))
        draw.rect(screen, "red", rect, 1)