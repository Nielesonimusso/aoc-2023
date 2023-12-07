import re
from math import pow
from collections import defaultdict

card_contents_match = re.compile(r'Card\s+(?P<card>\d+):(?P<winning>(?:\s+\d+)+)\s\|(?P<numbers>(?:\s+\d+)+)')
number_match = re.compile(r'\s+(?P<number>\d+)')

owned_cards = defaultdict(lambda: 1)

with open("data.txt", "r") as file:
    for line in file:
        card = card_contents_match.match(line)
        card_number = int(card["card"])
        winning = {int(m["number"]) for m in number_match.finditer(card["winning"])}
        numbers = {int(m["number"]) for m in number_match.finditer(card["numbers"])}

        matches = numbers & winning
        print(f"owning {owned_cards[card_number]} of card {card_number} with {len(matches)} matches")
        for card in range(card_number+1, card_number+1+len(matches)):
            owned_cards[card]+=owned_cards[card_number]

print(sum(owned_cards.values()))