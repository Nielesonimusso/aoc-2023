with open("data.txt", "rb") as file:
    total = 0
    current = 0
    while len(new := file.read(1)) > 0:
        if new == b',':
            total += current
            current = 0
            continue

        new_int = int.from_bytes(new)
        current = ((current + new_int) * 17) & 255
    else:
        total += current
    print(total)
