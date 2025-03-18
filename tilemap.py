import pygame as pg
from pygame import *
from os import listdir
from pickle import loads, dumps
global CAMERA

TILE_NAMES = [
    None,
    "dirt",
    None,
    "grass",
    "stone",
    "stone_slab",
    "water_light",
    "bread",
]
class TileData:
    def __init__(self, solid = False):
        self.solid = solid
default = TileData()
solid = TileData(solid = True)
TILE_DATA = [
    default,
    solid,
    default,
    solid,
    solid,
    solid,
    default,
    default,
]
TILE_ASSETS = dict()
for path in listdir("assets/tiles"):
    if "." not in path:
        continue
    name = path.split(".")[0]
    TILE_ASSETS[name] = pg.image.load(f"assets/tiles/{path}")

TILE_SIZE = 16
class Tile:
    def __init__(self, tile: int, data: dict[str, any]):
        self.tile = tile
        self.data = data
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
class TileMap:
    def __init__(self, tiles: list[list[Tile|int]], width, height):
        self.tiles = []
        for y in range(height):
            self.tiles.append([])
            for x in range(width):
                if len(tiles) > y:
                    if len(tiles[y]) > x:
                        self.tiles[y].append(tiles[y][x])
                        continue
                self.tiles[y].append(0)
        self.width = width
        self.height = height
    
    def extend_height(self, height: int):
        if self.height < height:
            self.tiles.extend([[0 for _ in range(self.width)] for _ in range(self.height, height)])
            self.height = height
    def extend_width(self, width: int):
        if self.width < width:
            for y in range(self.height):
                self.tiles[y].extend([0 for _ in range(self.width, width)])
            self.width = width
    
    def get(self, x: int, y: int) -> Tile|int:
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
    
    def set(self, x: int, y: int, tile: Tile|int) -> bool:
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
    
    def draw(self, surface: Surface, camera: Vector2, debug = False):
        start = camera / TILE_SIZE
        (width, height) = surface.get_size()
        end = start + Vector2(width, height) / TILE_SIZE
        for y in range(int(start.y), int(end.y) + 1):
            for x in range(int(start.x), int(end.x) + 1):
                tile = self.get(x, y)
                pos = Vector2(x * TILE_SIZE, y * TILE_SIZE) - camera
                if tile == 2 and debug:
                    draw.rect(surface, Color(0, 255, 0), Rect(pos.x, pos.y, TILE_SIZE, TILE_SIZE), width=2)
                elif TILE_NAMES[tile] is not None:
                    img = TILE_ASSETS[TILE_NAMES[tile]]
                    if img is not None:
                        surface.blit(img, Rect(pos.x, pos.y, TILE_SIZE, TILE_SIZE))

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
    while True:
        for e in event.get():
            # print(e)
            match e.type:
                case pg.MOUSEWHEEL:
                    selected -= e.y
                    if selected < 0:
                        selected = len(TILE_NAMES) - 1
                    elif selected > len(TILE_NAMES) - 1:
                        selected = 0
                case pg.KEYDOWN if e.key == K_s:
                    print(f"[SAVED] {level_name}")
                    save_map(level_name, tilemap)
                case pg.QUIT:
                    exit()
                    quit()

        left, middle, right = mouse.get_pressed(3)
        tile_pos = Vector2(mouse.get_pos()) / (TILE_SIZE * 2)
        if middle:
            tile = tilemap.get(int(tile_pos.x), int(tile_pos.y))
            if tile is Tile:
                selected = tile.tile
            else:
                selected = tile
        if left or right:
            tilemap.extend_height(int(tile_pos.y) + 1)
            tilemap.extend_width(int(tile_pos.x) + 1)
            tilemap.set(int(tile_pos.x - camera.x), int(tile_pos.y - camera.y), selected if left else 0)
        
        screen.fill("cyan")
        # Draw Start
        tilemap.draw(screen, camera, debug=True)
        name = TILE_NAMES[selected]
        if name is not None:
            img: Surface = TILE_ASSETS[name].copy()
            img.set_alpha(255 / 2)
            screen.blit(img, Rect(int(tile_pos.x) * TILE_SIZE, int(tile_pos.y) * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        # Draw End
        window.blit(transform.scale(screen, window.get_size()), (0, 0))
        display.flip()
        clock.tick(60)
                