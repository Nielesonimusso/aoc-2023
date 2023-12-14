from itertools import pairwise
from functools import reduce

total = 0

with open("data.txt", "r") as file:
    for index, line in enumerate(file):
        numbers: list[int] = [int(number) for number in line.split(" ")]
        first_interpolated: list[int] = [numbers[0]]
        while any(n != 0 for n in numbers):
            numbers = [b - a for a,b in pairwise(numbers)]
            first_interpolated.append(numbers[0])
        history = reduce(lambda a, b: b - a, reversed(first_interpolated))
        print(f"previous for {index + 1} = {history}")
        total += history
print(total)