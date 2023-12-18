from dataclasses import dataclass
from enum import Enum
from collections.abc import Iterator
from itertools import chain
from functools import reduce, partial

class Direction(Enum):
    NORTH = (0, -1)
    WEST = (-1, 0)
    SOUTH = (0, 1)
    EAST = (1, 0)

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
    def x(self):
        return self.value[0]
    
    @property
    def y(self):
        return self.value[1]

@dataclass(order=True)
class Position:
    x: int
    y: int

    def __getitem__(self, key: bool) -> int:
        return self.x if key else self.y
    
    def moveNextTo(self, other: 'Position', direction: Direction) -> None:
        self.x, self.y = other.x + direction.x, other.y + direction.y
    
    def inSameLine(self, pos: 'Position', horizontal: bool) -> bool:
        return self[not horizontal] == pos[not horizontal]
    
    def closest(self, ps: 'Iterator[Position]', 
                high_to_low: bool, horizontal: bool) -> 'Position | None':
        comparator = int.__gt__ if high_to_low else int.__lt__
        aggregator_ = min if high_to_low else max
        aggregator = lambda x, y: y if x is None else aggregator_(x, y, key=lambda p: p[horizontal])
        return reduce(aggregator, (p for p in ps 
                            if comparator(p[horizontal], self[horizontal])), None)
    
    def freeze(self) -> tuple[int, int]:
        return (self.x, self.y)

class Map:
    def __init__(self):
        self.squares: list[Position] = list()
        self.rounds: list[Position] = list()
        self.width = 0
        self.height = 0

    def cycle(self) -> None:
        for direction in Direction:
            print(f"rolling {direction}...")
            self.roll(direction)

    def _diff(self, other: list[Position]) -> int:
        return len([r for r in other if r not in self.rounds])

    def roll(self, direction: Direction) -> None:
        high_to_low = direction in [Direction.SOUTH, Direction.EAST]
        horizontal = direction in [Direction.EAST, Direction.WEST]
        rounds = sorted((r for r in self.rounds), 
                        key=lambda x: x.x if horizontal else x.y, 
                        reverse=high_to_low)
        for i, r in enumerate(rounds): 
            if (obstacle := r.closest(
                    (o for o in chain(self.squares, rounds) 
                     if r.inSameLine(o, horizontal)), high_to_low, horizontal)) is not None:
                r.moveNextTo(obstacle, direction.opposite)
            else:
                if horizontal:
                    r.x = self.width - 1 if high_to_low else 0
                else:
                    r.y = self.height - 1 if high_to_low else 0
    
    def __str__(self):
        string = ""
        for y in range(self.height):
            for x in range(self.width):
                if Position(x, y) in self.rounds:
                    string += "O"
                elif Position(x, y) in self.squares:
                    string += "#"
                else:
                    string += "."
            string += "\n"
        return string

    def total_north_load(self) -> int:
        return sum(self.height - pos.y for pos in self.rounds)

with open("data.txt", "r") as file:
    map = Map()
    for row, line in enumerate(file):
        map.height += 1

        stripped = line.strip()
        map.width = len(stripped)

        for column, position in enumerate(stripped):
            match(position):
                case "#":
                    map.squares.append(Position(column, row))
                    continue
                case "O":
                    map.rounds.append(Position(column, row))
                case _:
                    continue
    print(map)

    loop_range = range(0)
    hashes: list[int] = list()
    round_lists: list[list[Position]] = list()

    for i in range(1000000000):
        # break early when there are no more cache misses caused by the cycle 
        #  i.e. the cycle repeats
        hash_: int = hash(tuple(sorted((r.freeze() for r in map.rounds))))
        print(i, hash_)
        if hash_ in hashes:
            print(f"map repeat at {hashes.index(hash_)} (total={len(hashes)})")
            loop_range = range(hashes.index(hash_), len(hashes))
            break
        else:
            hashes.append(hash_)
            round_lists.append(map.rounds.copy())
        map.cycle()

    looping_length = 1000000000 - loop_range.start
    loop_index = loop_range.start + (looping_length % len(loop_range))
    final_round_hash = hashes[loop_index]
    print(f"looping_length: {looping_length}; final value: "+
          f"(index: {loop_index}, hash: {final_round_hash})")
    final_round_list = round_lists[loop_index]
    print(sum(map.height - pos.y for pos in final_round_list))

    # print(map.total_north_load())
    