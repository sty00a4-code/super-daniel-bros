from settings import *
from pygame import *
from tilemap import *
from player import Input, Player
from entities import *

font.init()
init()
window = display.set_mode((1920 / 2, 1080 / 2))
screen = Surface((1920 / 4, 1080 / 4))
display.set_caption("Super Daniel Bros")
clock = time.Clock()

class Game:
    def __init__(self):
        self.camera = Vector2(0, 0)
        self.input = Input()
        self.player = Player(Vector2(0, 0))
        self.tilemap = load_map("test")
        self.player.start(self.tilemap)
        self.entities = []
    def draw(self, screen):
        self.tilemap.draw(screen, self.camera)
        for entity in self.entities:
            entity.draw(screen, self.camera)
        self.player.draw(screen, self.camera)
    def update(self, dt):
        # update input manager
        self.input.mouse(self.camera)
        for e in event.get():
            self.input.event(e)
            if e.type == QUIT:
                exit()
                quit()

        self.player.update(dt, self)
        for entity in self.entities:
            entity.update(dt, self)

        # update camera
        self.camera.x = self.player.rect.centerx - screen.get_width() / 2
        if self.camera.x < 0:
            self.camera.x = 0
        if self.camera.y < 0:
            self.camera.y = 0
        if self.camera.x > self.tilemap.width * TILE_SIZE - screen.get_width():
            self.camera.x = self.tilemap.width * TILE_SIZE - screen.get_width()
        if self.camera.y > self.tilemap.height * TILE_SIZE - screen.get_height():
            self.camera.y = self.tilemap.height * TILE_SIZE - screen.get_height()
        self.camera.x = int(self.camera.x)
        self.camera.y = int(self.camera.y)

game = Game()

while True:
    dt = min(clock.tick(FPS)/1000, 1) # time since last frame
    game.update(dt)

    window.fill("black")
    screen.fill("cyan")
    game.draw(screen)
    window.blit(transform.scale(screen, window.get_size()), (0, 0))
    display.flip()
    clock.tick(FPS)