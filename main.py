from pygame import *

init()
screen = display.set_mode((1920 / 2, 1080 / 2))
clock = time.Clock()
running = True

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    screen.fill("cyan")
    # Draw Start
    draw.rect(screen, Color(255, 0, 0), Rect(0, 0, 50, 50))
    # Draw End
    display.flip()
    clock.tick(60)

quit()
