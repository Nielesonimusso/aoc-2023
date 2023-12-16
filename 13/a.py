from typing import Generator, Any
from itertools import chain

def reflectedSequence(start: int, 
                      down_limit: int, 
                      up_limit: int) -> Generator[tuple[int, int], Any, Any]:
    up = start + 1
    down = start
    while up < up_limit and down >= down_limit:
        yield down, up
        up += 1
        down -= 1


class ColumnView:
    def __init__(self, rows: list[str]):
        self.__rows = rows

    
    def __len__(self):
        if len(self.__rows) > 0:
            return len(self.__rows[0])
        else:
            return 0

    def __getitem__(self, key: int | slice):
        if type(key) is int:
            if key >= 0 and key < len(self):
                return [row[key] for row in self.__rows]
            else:
                raise IndexError
        elif type(key) is slice:
            return NotImplemented
        else:
            raise IndexError
        
    def __setitem__(self, key, value):
        return NotImplemented


def reflectsColumn(pattern: list[str], column: int) -> bool:
    columns = ColumnView(pattern)
    return all(columns[a] == columns[b] for a,b 
               in reflectedSequence(column, 0, len(columns)))


def reflectsRow(pattern: list[str], row: int) -> bool:
     return all(pattern[a] == pattern[b] for a,b 
               in reflectedSequence(row, 0, len(pattern)))

def reflectionNumber(pattern: list[str]) -> int:
    rows = len(pattern)
    columns = len(ColumnView(pattern))
    for column in range(0, columns - 1):
        if reflectsColumn(pattern, column):
            return column + 1
    for row in range(0, rows - 1):
        if reflectsRow(pattern, row):
            return (row + 1) * 100
    raise RuntimeError

with open("data.txt", "r") as file:
    pattern: list[str] = list()
    notes = 0
    for index, line in enumerate(chain(file, [""])):
        stripped_line = line.strip()
        print(stripped_line)
        if len(stripped_line) == 0:
            try:
                reflection_number = reflectionNumber(pattern)
                print(f"found reflection! {reflection_number}")
                notes += reflection_number
            except RuntimeError:
                print(f"could not find reflection for pattern number {index}")
            pattern = list()
        else:
            pattern.append(stripped_line)
    print(notes)