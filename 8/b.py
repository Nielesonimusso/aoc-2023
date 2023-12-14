import re
from collections import defaultdict
from math import lcm

element_regex = re.compile(r'(?P<start>[A-Z]{3}) = \((?P<left>[A-Z]{3}), (?P<right>[A-Z]{3})\)')

with open("data.txt", "r") as file:
    instructions = file.readline().strip()
    
    network: dict[str | None, tuple[str | None, str | None]] = dict()
    network[None] = (None, None)
    nodes: dict[str, str | None] = dict()

    for line in file:
        element = element_regex.match(line)
        if element is not None:
            element = element.groupdict()
            network[element["start"]] = (element["left"], element["right"])
            if element["start"].endswith("A"):
                nodes[element["start"]] = element["start"]

    steps = 0
    z_map: dict[str, dict[str, list[tuple[int, int]]]] = {node: defaultdict(list) 
                                                          for node in nodes}
    
    try:
        while True:
            for index, instruction in enumerate(instructions):
                match instruction:
                    case "L":
                        nodes = {start_node: network[current_node][0] 
                                 for start_node, current_node in nodes.items()}
                    case "R":
                        nodes = {start_node: network[current_node][1] 
                                 for start_node, current_node in nodes.items()}
                steps += 1
                for start_node, current_node in nodes.items():
                    if current_node is not None and current_node.endswith("Z"):
                        if index in (i[0] for i in z_map[start_node][current_node]):
                            nodes[start_node] = None
                        z_map[start_node][current_node].append((index, steps))

                if all(node is None for node in nodes.values()):
                    raise StopIteration
    except StopIteration:
        print(f"\tthe z_map: {z_map}")
        # found that the ..Z nodes are always achieved at the end of the 
        #  instruction set. This could probably be used to solve this problem 
        #  in a much simpler fashion (not keeping track of multiple values),
        #  but at least this code shows the effort needed to get to the answer :)
        #  QUESTION WAS UNCLEAR, GOT HEAD STUCK IN CIRCLES
        loop_numbers = [(end_node, encounters[1][1] - encounters[0][1]) 
                        for end_node, encounters in 
                        [z_map[start_node].popitem() for start_node in nodes]]
        print(f"\tthe final loop numbers: {loop_numbers}")
        total_steps = lcm(*(loop[1] for loop in loop_numbers))
        print(f"\tcoming to total steps: {total_steps}")