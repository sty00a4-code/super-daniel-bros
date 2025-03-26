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
    TileData(name="grass", solid=True),
    TileData(name="grass_left", solid=True),
    TileData(name="grass_right", solid=True),
    TileData(name="spike", action="hurt"),
    TileData(name="water_light", action="dead"),
    TileData(name="flag",action="goal"),
    TileData(name="box_full", solid=True),
    TileData(name="box_left", solid=True),
    TileData(name="box_right", solid=True),
    TileData(name="stone", solid=True),
    TileData(name="stone_slab", solid=True),
    TileData(name="plant"),
    TileData(name="bush"),
    TileData(name="chiseled_marble", solid=True),
    TileData(name="window_marble", solid=True),
    TileData(name="marble", solid=True),
    TileData(name="marble_left", solid=True),
    TileData(name="marble_middle", solid=True),
    TileData(name="marble_right", solid=True),
    TileData(name="marble_slab", solid=True),
    TileData(name="pillar_top"),
    TileData(name="pillar"),
    TileData(name="pillar_bottom"),
    TileData(name="sand", solid=True),
    TileData(name="sandstone", solid=True),
    TileData(name="treibsand", solid=False),
    TileData(name="cactus", solid=True),
    TileData(name="bread", spawn=True),
    TileData(name="raspberry", spawn=True),
    TileData(name="cherries", spawn=True),
    TileData(name="tabasco", spawn=True),
    TileData(name="bomb", spawn=True),
    TileData(name="egg_gold", spawn=True),
    TileData(name="rat", spawn=True),
    TileData(name="cactus_middle", solid=True),
    TileData(name="junglgras", solid=True),
    TileData(name="jungldirt", solid=True),
    TileData(name="junglelog", solid=True),
    TileData(name="leaves", solid=True),
    TileData(name="bambusmid", solid=False),
    TileData(name="bambustop", solid=False),
    TileData(name="mud", solid=False),
    ]
TILE_EDITOR = [
    # 1
    ["dirt", "grass_left", "grass", "grass_right", "stone", "stone_slab", "plant", "bush",],
    # 2
    ["marble", "marble_left", "marble_middle", "marble_right", "pillar_top", "pillar", "pillar_bottom", "chiseled_marble", "window_marble"],
    # 3
    ["box_full", "box_left", "box_right", "flag", "spike", "water_light",],
    # 4
    ["sand", "sandstone", "treibsand", "cactus", "cactus_middle"],
    # 5
    ["bread", "raspberry", "cherries", "tabasco", "bomb", "egg_gold",],
    # 6
    ["rat",],
    #7
    ["junglgras","jungldirt","mud","junglelog","leaves","bambusmid","bambustop"]
]