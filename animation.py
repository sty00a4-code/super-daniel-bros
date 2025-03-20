from settings import *
from pygame import *
from tilemap import *
from entities.egg import *

"""ANIMATION SYSTEM

animation sets: folder at animations/[name]
animations:     file at animations/[name]/[animation name].anim

animation file format:
[speed]
[cycle?]
[sprite #0]
[sprite #1]
...

"""


class Animation:
    """Animation class consisting of a list of sprites and an animation speed"""

    def __init__(self, sprites: list[Surface], speed: float = 1, cycle=True):
        self.sprites = sprites
        self.speed = speed
        self.time = 0
        self.cycle = cycle

    def start(self):
        self.time = 0

    def update(self, dt: float):
        self.time += dt

    def idx(self) -> int:
        return int(self.time * self.speed)

    def sprite(self) -> Surface:
        """Returns the current frame of the animation dependent on the time

        Returns:
            Surface: the current frame
        """
        if len(self.sprites) == 1:
            return self.sprites[0]
        if self.cycle:
            return self.sprites[self.idx() % len(self.sprites)]
        else:
            return self.sprites[min(self.idx(), len(self.sprites) - 1)]


class AnimationSet:
    def __init__(self, animations: dict, default="idle"):
        self.animations = animations
        self.current = default

    def update(self, dt: float):
        self.animations[self.current].update(dt)

    def start(self):
        self.animations[self.current].start()

    def play(self, name: str):
        self.current = name
        self.start()

    def idx(self) -> int:
        return self.animations[self.current].idx()

    def sprite(self) -> Surface:
        return self.animations[self.current].sprite()


def load_animations(name: str) -> AnimationSet:
    animations = dict()
    for path in listdir(f"animations/{name}"):
        if path.endswith(".anim"):
            with open(f"animations/{name}/{path}", "r") as f:
                speed = float(f.readline().strip())
                default = "idle"
                cycle = bool(f.readline().strip())
                sprites = []
                frame_name = f.readline().strip()
                while len(frame_name) > 0:
                    if frame_name.startswith("default="):
                        default = frame_name.split("=")[1]
                    else:
                        sprites.append(image.load(frame_name))
                    frame_name = f.readline().strip()
                animation_name = path.split(".")[0]
                animations[animation_name] = Animation(sprites, speed, cycle)
    return AnimationSet(animations, default)
