from settings import *
import pygame as pg
from pygame import *
from os import listdir
from pickle import loads, dumps
from math import sin
from time import time_ns as t


# tile with special data in it
class Tile:
    def __init__(self, tile: int, spawn=None):
        self.tile = tile
        self.spawn = spawn

    def get(self, key: str) -> any:
        """get data

        Args:
            key (str): name of data

        Returns:
            any: data
        """
        if key in self.data:
            return self.data[key]

    def set(self, key: str, value: any):
        """set the data

        Args:
            key (str): name of data
            value (any): (new) data
        """
        self.data[key] = value

# load tile sprites
TILE_ASSETS = dict()
for path in listdir("assets/tiles"):
    if "." not in path:
        continue
    name = path.split(".")[0]
    TILE_ASSETS[name] = pg.image.load(f"assets/tiles/{path}")


# tile map class
class TileMap:
    def __init__(self, tiles: list[list[int]], width, height):
        self.tiles = []
        self.background_tiles = []
        self.spawn = (0, 0)
        # copy over everything
        for y in range(height):
            self.background_tiles.append([])
            self.tiles.append([])
            for x in range(width):
                self.background_tiles[y].append(0)
                if len(tiles) > y:
                    if len(tiles[y]) > x:
                        self.tiles[y].append(tiles[y][x])
                        continue
                self.tiles[y].append(0)
        self.width = width
        self.height = height

    def extend_height(self, height: int):
        if self.height < height:
            self.tiles.extend(
                [[0 for _ in range(self.width)] for _ in range(self.height, height)]
            )
            self.height = height

    def extend_width(self, width: int):
        if self.width < width:
            for y in range(self.height):
                self.tiles[y].extend([0 for _ in range(self.width, width)])
            self.width = width

    def get(self, x: int, y: int) -> Tile | int:
        """Gives back tile

        Args:
            x (int): x position in tiles
            y (int): y position in tiles

        Returns:
            Tile|int|None: tile ID or Tile with Data if any tile is there
        """
        if not (0 <= y < len(self.tiles)):
            return 0
        row = self.tiles[y]
        if not (0 <= x < len(row)):
            return 0
        return row[x]

    def get_rect(self, x: int, y: int) -> Rect:
        """Get the Rect at that position for collision handling

        Args:
            x (int): x position in tiles
            y (int): y position in tiles

        Returns:
            Rect: 16x16 Rect at that position
        """
        return Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def real_to_tile(self, x: float, y: float) -> tuple[int, int]:
        """Get the tile position of the real world position

        Args:
            x (float): x real world coordinate
            y (float): y real world coordinate

        Returns:
            tuple[int, int]: (x, y) in tile position
        """
        return (int(x / TILE_SIZE), int(y / TILE_SIZE))

    def set(self, x: int, y: int, tile: int) -> bool:
        """set tile at the position to `tile`

        Args:
            x (int): x tile position
            y (int): y tile position
            tile (Tile | int): new tile

        Returns:
            bool: successful
        """
        if not (0 <= y < len(self.tiles)):
            return False
        if not (0 <= x < len(self.tiles[y])):
            return False
        self.tiles[y][x] = tile
        return True

    def update(self, dt: float, game):
        start = game.camera / TILE_SIZE
        (width, height) = game.screen.get_size()
        end = start + Vector2(width, height) / TILE_SIZE
        for y in range(int(start.y), int(end.y) + 1):
            for x in range(int(start.x), int(end.x) + 1):
                tile = self.get(x, y)
                if tile is Tile:
                    tile = tile.tile
                if TILE_DATA[tile].spawn:
                    game.push_spawn(x, y, tile)
                    self.set(x, y, 0)

    def draw(self, surface: Surface, camera: Vector2, debug=False):
        start = camera / TILE_SIZE
        (width, height) = surface.get_size()
        end = start + Vector2(width, height) / TILE_SIZE
        for y in range(int(start.y), int(end.y) + 1):
            for x in range(int(start.x), int(end.x) + 1):
                tile = self.get(x, y)
                if tile is Tile:  # only want the id, no data
                    tile = tile.tile
                pos = (
                    Vector2(x * TILE_SIZE, y * TILE_SIZE) - camera
                )  # position relative to the camera
                if tile == 2 and debug:  # goal tile
                    draw.rect(
                        surface,
                        Color(0, 255, 0),
                        Rect(pos.x, pos.y, TILE_SIZE, TILE_SIZE),
                        width=2,
                    )
                elif TILE_DATA[tile].name is not None:  # tile exists
                    img = TILE_ASSETS[TILE_DATA[tile].name]  # get image
                    if img is not None:
                        # item tiles move up and down
                        if TILE_DATA[tile].collectible:
                            surface.blit(
                                img,
                                Rect(
                                    pos.x,
                                    pos.y + sin(t() / 200_000_000 + x * y) * 2,
                                    TILE_SIZE,
                                    TILE_SIZE,
                                ),
                            )
                        else:
                            surface.blit(img, Rect(pos.x, pos.y, TILE_SIZE, TILE_SIZE))
        if debug:
            draw.rect(
                surface,
                Color(0, 0, 255),
                Rect(
                    self.spawn[0] * TILE_SIZE - camera.x,
                    self.spawn[1] * TILE_SIZE - camera.y,
                    TILE_SIZE,
                    TILE_SIZE,
                ),
                width=2,
            )


def load_map(name: str) -> TileMap:
    with open(f"level/{name}.pickle", "rb") as file:
        return loads(file.read())


def save_map(name: str, tilemap: TileMap):
    with open(f"level/{name}.pickle", "wb") as file:
        file.write(dumps(tilemap))


if __name__ == "__main__":
    from sys import argv
    from os.path import exists

    argv.pop(0)
    if len(argv) < 1:
        print("[ERROR] No level name given")
        exit(1)
    level_name = argv.pop(0)

    if not exists(f"level/{level_name}.pickle"):
        save_map(level_name, TileMap([[0]], 1, 1))
    tilemap = load_map(level_name)

    init()
    window = display.set_mode((1920 / 2, 1080 / 2))
    screen = Surface((1920 / 4, 1080 / 4))
    display.set_caption(f"Level: {level_name}")
    clock = time.Clock()

    selected = 1
    camera = Vector2(0, 0)
    move = Vector2(0, 0)
    while True:
        dt = clock.tick(FPS) / 1000
        left, middle, right = mouse.get_pressed(3)
        tile_pos = (Vector2(mouse.get_pos()) + camera * 2) // (TILE_SIZE * 2)
        for e in event.get():
            # print(e)
            if e.type == MOUSEWHEEL:
                selected -= e.y
                if selected < 0:
                    selected = len(TILE_DATA) - 1
                elif selected > len(TILE_DATA) - 1:
                    selected = 0
            elif e.type == KEYDOWN:
                if e.key == K_s:
                    if e.mod & pg.KMOD_LCTRL:
                        print(f"[SAVED] {level_name}")
                        save_map(level_name, tilemap)
                    else:
                        move.y = 1
                elif e.key == K_w:
                    move.y = -1
                elif e.key == K_a:
                    move.x = -1
                elif e.key == K_d:
                    move.x = 1
                elif e.key == K_e:
                    tilemap.spawn = (tile_pos.x, tile_pos.y)
            elif e.type == KEYUP:
                if e.key == K_s and move.y > 0:
                    move.y = 0
                elif e.key == K_w and move.y < 0:
                    move.y = 0
                elif e.key == K_a and move.x < 0:
                    move.x = 0
                elif e.key == K_d and move.x > 0:
                    move.x = 0
            elif e.type == QUIT:
                exit()
                quit()

        if middle:
            tile = tilemap.get(int(tile_pos.x), int(tile_pos.y))
            if tile is Tile:
                selected = tile.tile
            else:
                selected = tile
        if left or right:
            tilemap.extend_height(int(tile_pos.y) + 1)
            tilemap.extend_width(int(tile_pos.x) + 1)
            tilemap.set(int(tile_pos.x), int(tile_pos.y), selected if left else 0)

        camera += move * 500 * dt
        camera.x = int(camera.x)
        camera.y = int(camera.y)

        screen.fill("cyan")
        # Draw Start
        tilemap.draw(screen, camera, debug=True)
        name = TILE_DATA[selected].name
        if name is not None:
            img: Surface = TILE_ASSETS[name].copy()
            img.set_alpha(255 / 2)
            screen.blit(
                img,
                Rect(
                    int(tile_pos.x) * TILE_SIZE - camera.x,
                    int(tile_pos.y) * TILE_SIZE - camera.y,
                    TILE_SIZE,
                    TILE_SIZE,
                ),
            )
        draw.rect(
            screen,
            Color(255, 255, 255, 255 // 2),
            Rect(
                0 - camera.x,
                0 - camera.y,
                tilemap.width * TILE_SIZE,
                tilemap.height * TILE_SIZE,
            ),
            width=2,
        )
        # Draw End
        window.blit(transform.scale(screen, window.get_size()), (0, 0))
        display.flip()
        clock.tick(60)
