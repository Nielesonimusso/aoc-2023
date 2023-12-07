import re
from math import pow

total = 0

card_contents_match = re.compile(r'Card\s+(?P<card>\d+):(?P<winning>(?:\s+\d+)+)\s\|(?P<numbers>(?:\s+\d+)+)')
number_match = re.compile(r'\s+(?P<number>\d+)')

with open("data.txt", "r") as file:
    for line in file:
        card = card_contents_match.match(line)
        card_number = int(card["card"])
        winning = {int(m["number"]) for m in number_match.finditer(card["winning"])}
        numbers = {int(m["number"]) for m in number_match.finditer(card["numbers"])}

        matches = numbers & winning
        print(f"matches for card {card_number}: {matches}")

        total += int(pow(2,len(matches)-1))

print(total)