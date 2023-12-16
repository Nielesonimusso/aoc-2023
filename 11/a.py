import re
from typing import NamedTuple
from itertools import permutations

class Position(NamedTuple):
    x: int
    y: int

with open("data.txt", "r") as file:
    galaxies: list[Position] = list()
    picture_width = 0
    picture_height = 0
    
    for row, line in enumerate(file):
        if picture_width == 0:
            picture_width = len(line.strip())
        for galaxy in re.finditer('#', line.strip()):
            galaxies.append(Position(galaxy.start(), row))
        picture_height += 1

    print(f"galaxies: {len(galaxies)}")
    filled_rows = {position.y for position in galaxies}
    filled_columns = {position.x for position in galaxies}

    empty_rows = [row for row in range(0, picture_height) 
                  if row not in filled_rows]
    empty_columns = [column for column in range(0, picture_width) 
                     if column not in filled_columns]
    
    print(f"empty rows: {empty_rows}")
    print(f"empty columns: {empty_columns}")
    
    pairs = permutations(galaxies, 2)
    total_distance = 0

    for first, second in pairs:
        row_range = range(*sorted([first.y, second.y]))
        column_range = range(*sorted([first.x, second.x]))

        empty_rows_in_range = [row for row in empty_rows 
                               if row in row_range]
        empty_columns_in_range = [column for column in empty_columns 
                                  if column in column_range]

        total_distance += (len(row_range) + len(column_range) + 
                           len(empty_rows_in_range) + 
                           len(empty_columns_in_range))
        
    print(total_distance / 2)