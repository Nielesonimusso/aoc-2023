from enum import Flag, auto
from dataclasses import dataclass
from itertools import chain

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
            
    @property
    def vector(self) -> tuple[int, int]:
        match(self):
            case Direction.NORTH:
                return (0, -1)
            case Direction.EAST:
                return (1, 0)
            case Direction.SOUTH:
                return (0, 1)
            case Direction.WEST:
                return (-1, 0)

    @property
    def horizontal(self) -> bool:
        return self in (Direction.EAST, Direction.WEST)
    
    @property
    def vertical(self) -> bool:
        return self in (Direction.NORTH, Direction.SOUTH)
    
    @staticmethod
    def fromVector(vector: tuple[int, int]) -> 'Direction':
        match vector:
            case (0, -1):
                return Direction.NORTH
            case (1, 0):
                return Direction.EAST
            case (0, 1):
                return Direction.SOUTH
            case (-1, 0) | _:
                return Direction.WEST
    
    @staticmethod
    def fromTile(tile: str) -> 'Direction':
        return Direction(int.from_bytes(bytes(tile, 'ascii')) - 97)
    
    def toTile(self) -> str:
        return bytes([self.value + 97]).decode('ascii')
    
    def turn(self, flip: bool) -> 'Direction':
        v = self.vector
        return Direction.fromVector((-v[1] if flip else v[1], 
                                     -v[0] if flip else v[0])) 
    

@dataclass
class Position:
    x: int
    y: int

    def __add__(self, direction: Direction) -> 'Position':
        self.x += direction.vector[0]
        self.y += direction.vector[1]
        return self

    def copy(self) -> 'Position':
        return Position(self.x, self.y)
    
    def __repr__(self) -> str:
        return f"Position({self.x}, {self.y})"
    
class Beam:
    def __init__(self, position: Position, direction: Direction):
        self.position = position
        self.direction = direction

    def action(self, tile: str) -> 'Beam | None':
        match tile:
            case "/" | "%":
                self.direction = self.direction.turn(True)
            case "\\" | "&":
                self.direction = self.direction.turn(False)
            case "|" | "I":
                if self.direction.horizontal:
                    self.direction = Direction.NORTH
                    return Beam(self.position.copy(), Direction.SOUTH)
            case "-" | "=":
                if self.direction.vertical:
                    self.direction = Direction.EAST
                    return Beam(self.position.copy(), Direction.WEST)
            case "." | "#" | _:
                pass

    def __repr__(self) -> str:
        return f"Beam({self.position}, {self.direction})"
    
    def step(self) -> None:
        self.position += self.direction

energized = {
    "/": "%",
    "\\": "&",
    "|": "I",
    "-": "="
}

def energize(field: list[str], position: Position, 
             direction: Direction) -> bool:
    tile = field[position.y][position.x]
    new_tile: str = tile
    if tile in energized:
         new_tile = energized[tile]
    elif tile not in energized.values():
        dir_tile = Direction.fromTile(tile)
        if direction in dir_tile:
            return False
        else:
            new_tile = (dir_tile | direction).toTile()
    field[position.y] = (field[position.y][:position.x] + 
                              new_tile + 
                              field[position.y][position.x + 1:])
    return True

with open("data.txt", "r") as file:
    
    initial_field: list[str] = list()
    for line in file:
        initial_field.append(line.strip().replace(".", "a"))

    starting_top = [Beam(Position(i, 0), Direction.SOUTH) 
                    for i in range(len(initial_field[0]))]
    starting_bottom = [Beam(Position(i, len(initial_field) - 1), Direction.NORTH) 
                       for i in range(len(initial_field[0]))]
    
    starting_left = [Beam(Position(0, i), Direction.EAST) 
                     for i in range(len(initial_field))]
    starting_right = [Beam(Position(len(initial_field[0]) - 1, i), Direction.WEST) 
                      for i in range(len(initial_field))]
    
    maximum_energy = 0
    for starting_beam in chain(starting_top, starting_bottom, 
                               starting_left, starting_right):
        beam_name = (f"{starting_beam.position.x}-".rjust(4, '0')+
                     f"{starting_beam.position.y}-".rjust(4, '0')+
                     f"{starting_beam.direction.value}")
        field = initial_field.copy()
        beams = [starting_beam]
        while len(beams) > 0:
            new_beams = list()
            remove_beams = list()
            for beam in beams:
                tile = field[beam.position.y][beam.position.x]
                if energize(field, beam.position, beam.direction):
                    new_beam = beam.action(tile)
                    beam.step()

                    if new_beam is not None:
                        new_beams.append(new_beam)
                    if (beam.position.y not in range(len(field)) 
                        or beam.position.x not in range(len(field[0]))):
                        remove_beams.append(beam)
                else:
                    remove_beams.append(beam)
            beams = [beam for beam in beams if beam not in remove_beams] + new_beams
        energy = len([tile for line in field for tile in line 
                      if tile not in list(energized.keys()) + ['a']])
        maximum_energy = max(maximum_energy, energy)
        with open(f"final_fields/{str(energy).rjust(4, '0')}_{beam_name}.txt", "w") as field_file:
            field_file.writelines([line + "\n" for line in field])
    print(maximum_energy)