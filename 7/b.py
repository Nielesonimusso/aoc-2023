from enum import IntEnum
from collections import defaultdict
from functools import cached_property
import re

card_ordering = "AKQT987654321J"

class Type(IntEnum):
    FIVE=1
    FOUR=2
    FULL=3
    THREE=4
    TWO=5
    ONE=6
    HIGH=7

    def __str__(self):
        return self.name

class Hand:
    hand_regex = re.compile(r'(?P<hand>[1-9AKQJT]{5})\s+(?P<bid>\d+)')

    def __init__(self, cards: str, bid: int):
        self.cards = cards
        self.bid = bid

    @cached_property
    def type(self) -> Type:
        contents = defaultdict(int)
        for card in self.cards:
            contents[card] += 1

        jokers = contents["J"]
        del contents["J"]
        if len(contents) > 0:
            contents[max(contents, key=contents.__getitem__)] += jokers
            composition = [*contents.values()]

            if 5 in composition:
                return Type.FIVE
            if 4 in composition:
                return Type.FOUR
            if 3 in composition and 2 in composition:
                return Type.FULL
            if 3 in composition:
                return Type.THREE
            if composition.count(2)==2:
                return Type.TWO
            if 2 in composition:
                return Type.ONE
            return Type.HIGH
        else:
            return Type.FIVE
    
    def __lt__(self, other: 'Hand') -> bool:
        if self.type is not other.type:
            return self.type < other.type
        else:
            for self_card, other_card in zip(self.cards, other.cards):
                if self_card is not other_card:
                    return card_ordering.index(self_card) < card_ordering.index(other_card)
            return False
    
    def __str__(self) -> str:
        return f"{self.cards} ({self.type}): {self.bid}"

with open("data.txt", "r") as file:
    hands: list[Hand] = list()

    for line in file:
        hand_match = Hand.hand_regex.match(line)
        if hand_match is not None:
            hands.append(Hand(hand_match["hand"], int(hand_match["bid"])))

    hands.sort()
    for hand in hands:
        print(hand)

    total_winnings = sum(
        hand.bid * (len(hands) - index) for index, hand in enumerate(hands))
    
    print(total_winnings)

