import re
from collections import namedtuple, defaultdict
from enum import Enum, Flag, auto
from functools import lru_cache

Position = namedtuple("Position", ["line", "character"])

class Direction(Flag):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()

    @property
    def opposite(self) -> 'Direction':
        match(self):
            case Direction.NORTH:
                return Direction.SOUTH
            case Direction.EAST:
                return Direction.WEST
            case Direction.SOUTH:
                return Direction.NORTH
            case Direction.WEST:
                return Direction.EAST

class TileType(Enum):
    VERT = Direction.NORTH | Direction.SOUTH
    HORI = Direction.EAST | Direction.WEST
    DEGL = Direction.NORTH | Direction.EAST
    DEGJ = Direction.NORTH | Direction.WEST
    DEG7 = Direction.SOUTH | Direction.WEST
    DEGF = Direction.SOUTH | Direction.EAST
    GRND = Direction(0)
    # in principle, the start tile type could go in any direct, but the actual
    #  directions should be determined based on the tile's surroundings (see 
    #  `Tile.type`)
    STRT = Direction.NORTH | Direction.EAST | Direction.SOUTH | Direction.WEST

    @staticmethod
    def fromCharacter(character: str) -> 'TileType':
        match(character):
            case "|":
                return TileType.VERT
            case "-":
                return TileType.HORI
            case "L":
                return TileType.DEGL
            case "J":
                return TileType.DEGJ
            case "7":
                return TileType.DEG7
            case "F":
                return TileType.DEGF
            case "S":
                return TileType.STRT
            case "." | _:
                return TileType.GRND
            
    def nextDirection(self, start: Direction) -> Direction:
        return self.value ^ start

class Tile:
    def __init__(self, type: TileType, position: Position):
        self.__type: TileType = type
        self.neighbours: dict[Direction, Tile] = defaultdict(Tile.nullTile)
        self.position = position
        self.on_walk: bool = False

    @staticmethod
    @lru_cache
    def nullTile():
        return Tile(TileType.GRND, Position(-1,-1))

    def nextTile(self, start: Direction) -> 'Tile':
        return self.neighbours[self.type.nextDirection(start)]
    
    def connect(self, other: 'Tile', direction: Direction) -> None:
        self.neighbours[direction] = other
        other.neighbours[direction.opposite] = self
    
    @property
    def is_start(self) -> bool:
        return self.__type is TileType.STRT

    @property
    def type(self):
        if not self.is_start:
            return self.__type
        
        connected_directions = Direction(0)
        for direction, neighbour in self.neighbours.items():
            if direction.opposite in neighbour.type.value:
                connected_directions |= direction

        return TileType(connected_directions)

    def __repr__(self):
        return f"Tile({self.__type}, {self.position})"
    
class TileMap:
    def __init__(self):
        self.tiles: list[list[Tile]] = list()
        self.start_tile: Tile = Tile.nullTile()

    def addLine(self, line: str) -> None:
        # first, build the new line of tiles from the incoming string
        new_line: list[Tile] = list()
        for index, character in enumerate(line.strip()):
            new_tile = Tile(TileType.fromCharacter(character), 
                            Position(len(self.tiles), index))
            # if the new tile is the start tile, assign it to the 
            #  `start_tile` member
            if new_tile.is_start:
                self.start_tile = new_tile
            # connect each tile with its previous one
            if len(new_line) > 0:
                new_tile.connect(new_line[-1], Direction.WEST)
            new_line.append(new_tile)

        # connect the new line of tiles with the previous line of tiles
        if len(self.tiles) > 0:
            for new_tile, previous_tile in zip(new_line, self.tiles[-1]):
                new_tile.connect(previous_tile, Direction.NORTH)
        # add the new line to the total set of tiles
        self.tiles.append(new_line)
            

class Walk:
    def __init__(self, tile: Tile, coming_from: Direction, distance: int):
        self.tile = tile
        self.coming_from = coming_from
        self.distance = distance

    def step(self):
        next_coming_from = self.tile.type.nextDirection(
            self.coming_from).opposite
        self.tile = self.tile.nextTile(self.coming_from)
        self.tile.on_walk = True
        self.coming_from = next_coming_from
        self.distance += 1
    
    def __repr__(self) -> str:
        return f"Walk({self.tile}, {self.coming_from}, {self.distance})"


with open("data.txt", "r") as file:
    # build the tile map
    tile_map = TileMap()
    for line in file:
        tile_map.addLine(line)

    # walk in one of the directions of that is available to the start tile
    walk_direction = next(iter(tile_map.start_tile.type.value))
    walk = Walk(tile_map.start_tile.neighbours[walk_direction], 
                walk_direction.opposite, 1)
    
    while not (walk.tile is tile_map.start_tile 
               or walk.tile is Tile.nullTile()):
        walk.step()

    # determine the amount of tiles inside the walked path
    tiles_inside = 0
    for line in tile_map.tiles:
        passed_directions = Direction(0)

        for tile in line:
            if tile.on_walk:
                passed_directions ^= tile.type.value
            elif (Direction.NORTH in passed_directions and 
                  Direction.SOUTH in passed_directions):
                tiles_inside += 1
    print(tiles_inside)
                