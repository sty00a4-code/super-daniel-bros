# Game
Holds the whole game state. This object is passed around to every update call

## Attributes
- `screen: Surface` - the game screen
- `camera: Vector2` - the camera position
- `input: Input` - the input manager
- `player: Player` - the main player
- `tilemap: TileMap` - the tilemap
- `entities: list[Entity]` - all the entities present
- `spawn_stack: list[tuple[int, int, Tile|int]]` - spawn queue

# Tile Map
It holds all the important level data. Levels are stored in `.pickle` files under the `level` folder. When running the `tilemap.py` with a level name as an arguement, you will open that level in the editor.

## Attributes
- `tiles: list[list[Tile|int]]` - the actual tiles as either an ID or `Tile` object
- `background_tiles: list[list[Tile|int]]` - like `tiles` but in the background
- `spawn: tuple[int, int]` - which tile the player spawns on
- `width: int` - the width of the tile map
- `height: int` - the height of the tile map

## Important Methods
- `update(self, dt: float, game: Game)` - used to put spawns in the `Game.spawn_stack` if spawner tiles are on screen.
- `draw(self, screen: Surface, camera: Vector2, debug: bool = False)` - draws only the visible tiles on the screen relative to the camera

# Tile
If extra data specifically for this tile is needed, like spawner or maybe a chest with content

## Attributes
- `tile: int` - the tile ID
- `spawn: bool` - if it is a spawner tile
