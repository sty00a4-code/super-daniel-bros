from settings import *
from pygame import *
from player_module.player import Player
from player_module.input import Input
from tilemap import load_map, TILE_SIZE, TILE_DATA, Tile
from entities import rat, collectible, item

class Game:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.camera = Vector2(0, 0)
        self.input = Input()
        self.player = Player(Vector2(0, 0))
        self.tilemap = load_map("test")
        self.player.start(self.tilemap)
        self.entities = []
        self.spawn_stack = []

    def draw(self):
        self.tilemap.draw(self.screen, self.camera)
        for entity in self.entities:
            entity.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)

    def push_spawn(self, x: int, y: int, tile: Tile):
        self.spawn_stack.append((x, y, tile))
    
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
    
    def update(self, dt):
        # update input manager
        self.input.mouse(self.camera)
        for e in event.get():
            self.input.event(e)
            if e.type == QUIT:
                exit()
                quit()

        self.player.update(dt, self)
        self.tilemap.update(dt, self)
        for spawn in self.spawn_stack:
            self.spawn(spawn[0], spawn[1], spawn[2])
        self.spawn_stack.clear()
        for entity in self.entities:
            entity.update(dt, self)

        # update camera
        self.camera.x = self.player.rect.centerx - self.screen.get_width() / 2
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