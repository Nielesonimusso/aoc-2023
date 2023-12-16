import re
from functools import lru_cache

line_regex = re.compile(r'(?P<springs>[.?#]+)\s(?P<groups>(?:\d+,)*\d+)')

@lru_cache
def templateHasSpace(template: str, remaining_groups: tuple):
    return (template.count("#") + template.count("?") >= sum(remaining_groups) and
            len(template) >= sum(remaining_groups) + len(remaining_groups) - 1)

@lru_cache
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
        if line_match := line_regex.match(line):
            springs = "?".join([line_match["springs"]] * 5)
            groups = tuple([int(group) for group in line_match["groups"].split(",")] * 5)

            line_options: list[str] = [springs]
            for index, group in enumerate(groups):
                remaining = groups[index+1:]
                line_options = [option for previous in line_options 
                                for option in optionsAfterAddingAmount(previous, group, remaining)]
                print(len(line_options))
            total_options += len(line_options)
            print("---")

    print(total_options)