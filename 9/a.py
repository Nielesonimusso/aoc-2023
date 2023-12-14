from itertools import pairwise

total = 0

with open("data.txt", "r") as file:
    for index, line in enumerate(file):
        numbers: list[int] = [int(number) for number in line.split(" ")]
        last_interpolated: list[int] = [numbers[-1]]
        while any(n != 0 for n in numbers):
            numbers = [b - a for a,b in pairwise(numbers)]
            last_interpolated.append(numbers[-1])
        print(f"next for {index + 1} = {sum(last_interpolated)}")
        total += sum(last_interpolated)
print(total)