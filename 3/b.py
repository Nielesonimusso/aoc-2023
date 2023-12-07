import re
from collections import namedtuple

total = 0
number_match = re.compile(r'\d+')
gear_match = re.compile(r'\*')
SpacedNumber = namedtuple('SpacedNumber', ["number", "first", "last"])

class InfiniteString(str):
    def __getitem__(self, key):
        if super().__len__() > 0 and key >= 0 and key < super().__len__():
            return super().__getitem__(key)
        else:
            return "."

class InfiniteStringWithNumberMatches(InfiniteString):
    @property
    def numbers(self):
        return (SpacedNumber(int(match[0]), match.start(), match.end() - 1) 
                for match in number_match.finditer(self))

def linesWithContext():
    top = InfiniteStringWithNumberMatches()
    middle = InfiniteStringWithNumberMatches()
    bottom = InfiniteStringWithNumberMatches()
    with open("data.txt", "r") as file:
        for line in file:
            top = middle
            middle = bottom
            bottom = InfiniteStringWithNumberMatches(line.strip())
            yield (top, middle, bottom)
    yield (middle, bottom, InfiniteStringWithNumberMatches())
    

for row, lines in enumerate(linesWithContext()):
    for potential_gear in gear_match.finditer(lines[1]):
        column = potential_gear.start()
        numbers = list()
        for line_index in range(3):
            for spaced_number in lines[line_index].numbers:
                if spaced_number.first <= column + 1 and spaced_number.last >= column - 1:
                    numbers.append(spaced_number.number)
        if len(numbers) == 2:
            print(f"gear at ({row},{column+1}) with numbers {numbers}")
            total += numbers[0] * numbers[1]

print(total)