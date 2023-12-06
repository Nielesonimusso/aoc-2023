import re
from functools import reduce

total = 0

game_match = re.compile(r'Game (?P<id>\d+):\s(?P<rounds>(?:[^;];?)*[^;\n])')

with open("data.txt", "r") as file:
    for line in file:
        id, rounds = game_match.match(line).groups()
        max_round_map = dict(
            red=0,
            green=0,
            blue=0
        )
        for round in rounds.split(';'):
            for entry in round.split(','):
                amount, color = entry.strip().split(' ')
                max_round_map[color] = max(max_round_map[color], int(amount))
        power = reduce(lambda x,y: x * y, max_round_map.values())
        print(f"{id} {max_round_map} {power}")
        total += power

print(total)