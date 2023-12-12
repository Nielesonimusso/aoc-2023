import re
from math import sqrt, floor

numbers_regex = re.compile(r'\d+')

total = 1

with open("data.txt", "r") as file:
    time = int("".join(n for n in numbers_regex.findall(file.readline())))
    record = int("".join(n for n in numbers_regex.findall(file.readline())))

    D = time * time - 4 * record
    
    hold_start = (time - sqrt(D))/2
    hold_end = (time + sqrt(D))/2
    
    hold_range = range(floor(hold_start) + 1, floor(hold_end) + 1)
    number_of_ways = len(hold_range)
    print(f"for time {time} should hold within range {hold_range} ({number_of_ways} options)")

    total *= number_of_ways

print(total)