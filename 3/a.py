import re

total = 0

class InfiniteString(str):
    def __getitem__(self, key):
        if super().__len__() > 0 and key >= 0 and key < super().__len__():
            return super().__getitem__(key)
        else:
            return "."

def linesWithContext():
    top = InfiniteString()
    middle = InfiniteString()
    bottom = InfiniteString()
    with open("data.txt", "r") as file:
        for line in file:
            top = middle
            middle = bottom
            bottom = InfiniteString(line.strip())
            yield (top, middle, bottom)
    yield (middle, bottom, InfiniteString())
    
number_match = re.compile(r'\d+')

for lines in linesWithContext():
    for number in number_match.finditer(lines[1]):
        span = number.span()
        try:
            for line_index in range(3):
                for column_index in range(span[0] - 1, span[1] + 1):
                    character = lines[line_index][column_index]
                    if not character.startswith(".") and not character.isdigit():
                        print(f"{number[0]} is a part number ({character})")
                        total += int(number[0])
                        raise StopIteration
        except StopIteration:
            pass

print(total)