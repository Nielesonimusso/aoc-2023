from collections import defaultdict

with open("data.txt", "r") as file:

    weights: dict[int, int] = defaultdict(int)
    earliest_block: dict[int, int] = defaultdict(lambda: -1)
    total_rows = 0

    for row, line in enumerate(file):
        stripped = line.strip()
        for column, position in enumerate(stripped):
            match(position):
                case "#":
                    earliest_block[column] = row
                    continue
                case "O":
                    actual_row = earliest_block[column] + 1
                    earliest_block[column] += 1
                    weights[actual_row] += 1
                case "." | _:
                    continue
        total_rows += 1

    total_weight = sum(weight * (total_rows - row)
                       for row, weight in weights.items())
    print(total_weight)