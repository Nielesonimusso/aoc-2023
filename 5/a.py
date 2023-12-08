with open("data.txt", "r") as file:
    values = [int(p) for p in file.readline().split(" ")[1:]]
    new_values = values.copy()
    print(f"starting values: {values}")

    for line in file:
        # skip empty line
        if len(line.strip()) == 0:
            continue

        # start a new mapping when the line says "map"
        if 'map' in line:
            values = new_values
            new_values = values.copy()
            print(f"mapped: {values}")
            continue

        destination_start, source_start, length = [int(p.strip()) for p in line.split(" ")]
        for index, value in enumerate(values):
            if value in range(source_start, source_start + length):
                new_values[index] = destination_start + (value - source_start)
    
    print(f"locations: {new_values}")
    print(f"lowest location: {min(new_values)}")

