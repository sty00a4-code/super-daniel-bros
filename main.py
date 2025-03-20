from settings import *
from pygame import *
from tilemap import *
from player_module.player import Input, Player
from entities import *
from game import Game

font.init()
init()
window = display.set_mode((1920 / 2, 1080 / 2))
screen = Surface((1920 / 4, 1080 / 4))
display.set_caption("Super Daniel Bros")
clock = time.Clock()

game = Game(screen)

while True:
    dt = min(clock.tick(FPS) / 1000, 1)  # time since last frame
    game.update(dt)

    window.fill("black")
    screen.fill("cyan")
    game.draw()
    window.blit(transform.scale(game.screen, window.get_size()), (0, 0))
    display.flip()
    clock.tick(FPS)
