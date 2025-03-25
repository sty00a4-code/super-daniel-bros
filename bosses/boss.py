from settings import *
from pygame import *

class Boss:
    def __init__(self):
        self.rect = Rect(0, 0, TILE_SIZE, TILE_SIZE)
        self.vel = Vector2(0, 0)
        self.dir = 1
    def start(self, game):
        pass
    def update(self, dt: float, game):
        pass
    def draw(self, screen: Surface, camera: Vector2):
        rect = Rect(self.rect.x - camera.x, self.rect.y - camera.y, self.rect.w, self.rect.y)
        draw.rect(screen, Color(255, 0, 0), rect)
    def die(self, game):
        pass