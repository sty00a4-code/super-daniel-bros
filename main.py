from settings import *
from pygame import *
from tilemap import *
from player import *
from entities import *

font.init()
init()
window = display.set_mode((1920 / 2, 1080 / 2))
screen = Surface((1920 / 4, 1080 / 4))
display.set_caption("Super Daniel Bros")
clock = time.Clock()
camera = Vector2(0, 0)
input = Input()
player = Player(Vector2(0, 0))
tilemap = load_map("test")
player.start(tilemap)
ENTITIES = [
    Entity(Rect(100, 0, TILE_SIZE, TILE_SIZE))
]

while True:
    dt = clock.tick(FPS)/1000
    for e in event.get():
        input.event(e)
        if e.type == QUIT:
            exit()
            quit()

    player.update(dt, tilemap, input)
    for entity in ENTITIES:
        entity.update(dt, tilemap, ENTITIES, player)

    camera.x = player.rect.centerx - screen.get_width() / 2
    if camera.x < 0:
        camera.x = 0
    if camera.y < 0:
        camera.y = 0
    if camera.x > tilemap.width * TILE_SIZE - screen.get_width():
        camera.x = tilemap.width * TILE_SIZE - screen.get_width()
    if camera.y > tilemap.height * TILE_SIZE - screen.get_height():
        camera.y = tilemap.height * TILE_SIZE - screen.get_height()
    camera.x = int(camera.x)
    camera.y = int(camera.y)

    window.fill("black")
    screen.fill("cyan")
    # Draw Start
    tilemap.draw(screen, camera)
    for entity in ENTITIES:
        entity.draw(screen, camera)
    player.draw(screen, camera)
    # Draw End
    window.blit(transform.scale(screen, window.get_size()), (0, 0))
    display.flip()
    clock.tick(FPS)