import scenes.gorilla
from settings import *
from pygame import *
from player_module.player import Player
from player_module.input import Input
from tilemap import load_map, TILE_SIZE, TILE_DATA, Tile
from entities import rat, collectible, item
from game_state import GameState
from bosses import raven, gorilla
from scenes.scene import Scene
import scenes

LEVEL = ["grass", "gorilla"]
GOAL_TIME = 1
DEAD_TIME = 1


class Game:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.camera = Vector2(0, 0)
        self.input = Input()
        self.player = Player(Vector2(0, 0))
        self.level = 0
        self.tilemap = None
        self.state = GameState.Game
        self.entities = []
        self.spawn_stack = []
        self.scene = None
        self.timer = 0
        self.boss = None
        self.start(LEVEL[self.level])

    def start(self, name):
        print(f"[LOADED] {name}")
        self.input.start()
        self.boss = None
        self.tilemap = load_map(name)
        self.player.start(self.tilemap)
        self.state = GameState.Game
        self.entities = []
        self.spawn_stack = []
        self.scene: Scene = None
        self.timer = 0
        if self.tilemap.boss is not None:
            self.state = GameState.Scene
            if self.tilemap.boss == "raven":
                self.boss = raven.Raven()
            elif self.tilemap.boss == "scorpion":
                self.boss = raven.Raven()  # TODO
            elif self.tilemap.boss == "gorilla":
                self.boss = gorilla.Gorilla()
                self.boss.rect.x = 480 - 64
                self.scene = scenes.gorilla.scene

    def draw(self):
        self.tilemap.draw(self.screen, self.camera)
        if self.boss is not None:
            self.boss.draw(self)
        for entity in self.entities:
            entity.draw(self.screen, self.camera)
        self.player.draw(self)

    def push_spawn(self, x: int, y: int, tile: Tile):
        self.spawn_stack.append((x, y, tile))

    def spawn_entity(self, entity):
        self.entities.append(entity)

    def spawn(self, x: int, y: int, tile: Tile):
        entity = None
        if TILE_DATA[tile].name in COLLECTIBLES:
            entity = collectible.Collectible(TILE_DATA[tile].name)
        elif TILE_DATA[tile].name in ITEMS:
            entity = item.Item(TILE_DATA[tile].name)
        elif TILE_DATA[tile].name == "rat":
            entity = rat.Rat()
        else:
            print(f"[ERROR] unknown entity '{TILE_DATA[tile].name}'")
            return
        entity.rect.x = x * TILE_SIZE
        entity.rect.y = y * TILE_SIZE
        self.entities.append(entity)
        print(f"[SPAWNED] {entity.__class__}")

    def goal(self):
        self.state = GameState.Goal

    def dead(self):
        self.state = GameState.Dead

    def next_level(self):
        self.level += 1
        if self.level >= len(LEVEL):
            quit()
            exit()
        self.start(LEVEL[self.level])

    def update(self, dt):
        # update input manager
        self.input.mouse(self.camera)
        for e in event.get():
            if self.state == GameState.Game:
                self.input.event(e)
            if e.type == QUIT:
                exit()
                quit()
        if self.state == GameState.Game:
            self.player.update(dt, self)
            self.tilemap.update(dt, self)
            for spawn in self.spawn_stack:
                self.spawn(spawn[0], spawn[1], spawn[2])
            self.spawn_stack.clear()
            for entity in self.entities:
                entity.update(dt, self)
            if self.boss is not None:
                self.boss.update(dt, self)
            # update camera
            self.camera.x = self.player.rect.centerx - self.screen.get_width() / 2
            self.camera.y = self.player.rect.centery - self.screen.get_height() / 2
        elif self.state == GameState.Scene:
            self.scene.update(dt, self)
            if self.scene.index >= len(self.scene.actions):
                self.state = GameState.Game
        elif self.state == GameState.Goal:
            self.player.update(dt, self)
            if self.timer < GOAL_TIME:
                self.timer += dt
            else:
                self.next_level()
        elif self.state == GameState.Dead:
            if self.timer < DEAD_TIME:
                self.timer += dt
            else:
                self.start(LEVEL[self.level])

        # constrain camera
        if self.camera.x < 0:
            self.camera.x = 0
        if self.camera.y < 0:
            self.camera.y = 0
        if self.camera.x > self.tilemap.width * TILE_SIZE - self.screen.get_width():
            self.camera.x = self.tilemap.width * TILE_SIZE - self.screen.get_width()
        if self.camera.y > self.tilemap.height * TILE_SIZE - self.screen.get_height():
            self.camera.y = self.tilemap.height * TILE_SIZE - self.screen.get_height()
        self.camera.x = int(self.camera.x)
        self.camera.y = int(self.camera.y)

        self.input.reset()
