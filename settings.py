FPS = 120
GRAVITY = 50
TILE_SIZE = 16
COLLECTIBLES = {
    "bread": 5,
    "raspberry": 2,
    "cherries": 1,
}
ITEMS = ["tabasco", "bomb"]

# special tile data
class TileData:
    def __init__(
        self,
        name: str = None,
        solid=False,
        action: str = None,
        collectible=False,
        spawn=False,
    ):
        self.name = name
        self.solid = solid
        self.action = action
        self.collectible = collectible
        self.spawn = spawn
default = TileData()  # no data
# tile data for every tile id
TILE_DATA = [
    default,
    TileData(name="dirt", solid=True),
    TileData(action="goal"),
    TileData(name="grass", solid=True),
    TileData(name="stone", solid=True),
    TileData(name="stone_slab", solid=True),
    TileData(name="water_light"),
    TileData(name="bread", spawn=True),
    TileData(name="cherries", spawn=True),
    TileData(name="raspberry", spawn=True),
    TileData(name="pillar"),
    TileData(name="pillar_bottom"),
    TileData(name="pillar_top"),
    TileData(name="marble", solid=True),
    TileData(name="tabasco", spawn=True),
    TileData(name="rat", spawn=True),
    TileData(name="sand_2", solid=True),
    TileData(name="sandstone", solid=True),
]