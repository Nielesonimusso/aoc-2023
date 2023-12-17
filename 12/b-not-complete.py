import re
from functools import cache

line_regex = re.compile(r'(?P<springs>[.?#]+)\s(?P<groups>(?:\d+,)*\d+)')

@cache
def templateHasSpace(template: str, remaining_groups: tuple):
    return (template.count("#") + template.count("?") >= sum(remaining_groups) and
            len(template) >= sum(remaining_groups) + len(remaining_groups) - 1)

@cache
def optionsAfterAddingAmount(template: str, amount: int, remaining_groups: tuple) -> list[str]:

    options: list[str] = list()

    for start in range(0, len(template) - amount):
        fill_area = template[start:start+amount]

        if all(c == "?" or c == "#" for c in fill_area):
            if start+amount == len(template):
                options.append('')
            elif template[start+amount] == "?" or template[start+amount] == ".":
                option = '.' + template[start+amount+1:]
                if templateHasSpace(option, remaining_groups):
                    options.append(option)

    return options
        
with open("data.txt", "r") as file:
    total_options = 0
    for index, line in enumerate(file):
        print(f"--- start {index} ---")
        if line_match := line_regex.match(line):
            springs = "?".join([line_match["springs"]] * 5)
            groups = tuple([int(group) for group in line_match["groups"].split(",")] * 5)
            print(f"springs: {springs}")
            print(f"groups: {groups}")

            line_options: list[str] = [springs]
            for group_idx, group in enumerate(groups):
                remaining = groups[group_idx+1:]
                line_options = [option for previous in line_options 
                                for option in optionsAfterAddingAmount(previous, group, remaining)]
                print(len(line_options))
            total_options += len(line_options)
        print(f"--- end {index} ---")

    print(total_options)