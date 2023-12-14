import re

element_regex = re.compile(r'(?P<start>[A-Z]{3}) = \((?P<left>[A-Z]{3}), (?P<right>[A-Z]{3})\)')

with open("data.txt", "r") as file:
    instructions = file.readline().strip()
    
    network: dict[str, tuple[str, str]] = dict()

    for line in file:
        element = element_regex.match(line)
        if element is not None:
            element = element.groupdict()
            network[element["start"]] = (element["left"], element["right"])

    node = "AAA"
    steps = 0

    try:
        while True:
            for instruction in instructions:
                match instruction:
                    case "L":
                        node = network[node][0]
                    case "R":
                        node = network[node][1]
                steps += 1
                if node == "ZZZ":
                    raise StopIteration
    except StopIteration:
        print(steps)