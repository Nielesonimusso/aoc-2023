# heavily based on https://github.com/Rtchaik/AoC-2023/blob/main/Day12/solution.py

import re
from itertools import groupby
from functools import cache

line_regex = re.compile(r'(?P<springs>[.?#]+)\s(?P<groups>(?:\d+,)*\d+)')

@cache
def totalOptionsRecursive(springs: str, groups: tuple) -> int:
    first_group = groups[0]
    remaining_groups = groups[1:]
    space_for_groups = sum(remaining_groups) + len(remaining_groups)
    first_options = ((padding, "."*padding + "#"*first_group + ".") for 
                     padding in range(0, len(springs) - space_for_groups))
    fitting_options = (len(option) for padding, option in first_options 
                       if re.match(rf'^[.?]{{{padding}}}[#?]{{{first_group}}}[.?]', 
                                   springs) is not None)
    if len(remaining_groups) > 0:
        return sum(totalOptionsRecursive(springs[option:], remaining_groups) 
                   for option in fitting_options)
    else:
        return sum('#' not in springs[option:] for option in fitting_options)


with open("data.txt", "r") as file:
    total_options = 0
    for index, line in enumerate(file):
        if line_match := line_regex.match(line):
            springs = "?".join([line_match["springs"]] * 5)
            groups = tuple([int(group) for group in line_match["groups"].split(",")] * 5)

            line_options = totalOptionsRecursive(springs+".", groups)
            total_options += line_options
            print(f"{index}: {line_options}")

    print(total_options)