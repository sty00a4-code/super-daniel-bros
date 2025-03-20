from pygame import *

class Input:
    """Input manager

    - left: K_a
    - right: K_d
    - jump: K_w
    - attack: K_n
    - throw: K_m
    """

    def __init__(self):
        self.left = False
        self.right = False
        self.jump = False
        self.attack = False
        self.throw = False
        self.cursor = Vector2(0, 0)

    def mouse(self, camera: Vector2):
        mouse_pos = mouse.get_pos()
        self.cursor.x = mouse_pos[0] / 2 + camera.x
        self.cursor.y = mouse_pos[1] / 2 + camera.y

    def event(self, event: event.Event):
        if event.type in [KEYDOWN, KEYUP]:
            if event.key == K_a:
                self.left = event.type == KEYDOWN
            elif event.key == K_d:
                self.right = event.type == KEYDOWN
            elif event.key == K_w:
                self.jump = event.type == KEYDOWN
            elif event.key == K_SPACE:
                self.throw = event.type == KEYDOWN