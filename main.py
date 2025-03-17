from pygame import *
from tilemap import *

init()
window = display.set_mode((1920 / 2, 1080 / 2))
screen = Surface((1920 / 4, 1080 / 4))
display.set_caption("Super Daniel Bros")
clock = time.Clock()
camera = Vector2(0, 0)
tilemap = load_map("test")

while True:
    for e in event.get():
        if e.type == QUIT:
            exit()
            quit()

    window.fill("black")
    screen.fill("cyan")
    # Draw Start
    tilemap.draw(screen, camera)
    # Draw End
    window.blit(transform.scale(screen, window.get_size()), (0, 0))
    display.flip()
    clock.tick(60)