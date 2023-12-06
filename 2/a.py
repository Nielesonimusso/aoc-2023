import re

sum = 0

max_map = dict(
    red=12,
    green=13,
    blue=14
)

game_match = re.compile(r'Game (?P<id>\d+):\s(?P<rounds>(?:[^;];?)*[^;\n])')

with open("data.txt", "r") as file:
    for line in file:
        id, rounds = game_match.match(line).groups()
        try:
            for round in rounds.split(';'):
                for entry in round.split(','):
                    amount, color = entry.strip().split(' ')
                    if int(amount) > max_map[color]:
                        raise StopIteration(f"{id}: {amount} > {max_map[color]} ({color})")
            sum += int(id)
        except StopIteration as e:
            print(e.value)

print(sum)