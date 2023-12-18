import re
from functools import cache
from time import sleep

def hashArea(area: list[str]) -> int:
    return hash(sum(hash(l) for l in area))

def printArea(area: tuple[str, ...]) -> None:
    right_side_up_area: tuple[str, ...] = area
    for _ in range(3):
        right_side_up_area = rotateArea(right_side_up_area)
    for line in right_side_up_area:
        print(line)

@cache
def cached_sorted_part(part: str) -> str:
    return "".join(sorted(part))

@cache
def cached_sorted_line(line: str) -> str:
    return "#".join("".join(cached_sorted_part(l)) for l in line.split("#"))

@cache
def rollArea(area: tuple[str, ...]) -> tuple[str, ...]:
    return tuple([cached_sorted_line(line) for line in area])

@cache
def rotateArea(area: tuple[str, ...]) -> tuple[str, ...]:
    new_area: list[str] = [""] * len(area[0])
    for line in area:
        for index, character in enumerate(line):
            new_area[index] = character + new_area[index]
    return tuple(new_area)

@cache
def cycleArea(area: tuple[str, ...]) -> tuple[str, ...]:
    cycled_area: tuple[str, ...] = area
    for _ in range(4):
        cycled_area = rotateArea(rollArea(cycled_area))
    return cycled_area

def loadOfArea(area: tuple[str, ...]) -> int:
    return sum(sum(c.start() + 1 for c in re.finditer("O", line)) for line in area)


input_area: list[str] = list()
past_areas: list[tuple[str, ...]] = list()
past_hashes: list[int] = list()
end: int = 1000000000
show_each: bool = False
shortcut: bool = True

with open("data.txt", "r") as file:
    for line in file:
        stripped = line.strip()
        if len(input_area) == 0:
            input_area = [""] * len(stripped)
        for index, character in enumerate(stripped):
            input_area[index] = character + input_area[index]

    area = tuple(input_area)
    for i in range(end):
        if show_each:
            printArea(area)
        if shortcut:
            hashed_area = hash(area)
            if hashed_area in past_hashes:
                print(f"FOUND LOOP at {i} (SAME AS {past_hashes.index(hashed_area)})")

                loop_end = len(past_areas) 
                loop_start = past_hashes.index(hashed_area)
                loop_length = loop_end - loop_start 

                loop_space = end - loop_start 
                loop_index = loop_space % loop_length 
                final_index = loop_start + loop_index 
                final_area = past_areas[final_index] 

                print(f"FINAL LOAD {loadOfArea(final_area)}")
                print(f"LOADS AROUND: {[loadOfArea(past_areas[final_index + a]) for a in range(-5, 6, 1)]}")

                break
            else:
                past_hashes.append(hashed_area)
                past_areas.append(area)
        elif i %(end/100)==0:
            # show progress by printing one . per 1%
            print(".", end="", flush=True)
        if show_each:
            print("---")
            sleep(1)
        area = cycleArea(area)

    if not shortcut:
        print(f"FINAL LOAD (NO SHORTCUT): {loadOfArea(area)}")
    for f in [cached_sorted_part, cached_sorted_line, 
              rollArea, rotateArea, cycleArea]:
        cache_ = f.cache_info()
        print(f"cache of {f.__wrapped__.__name__}: {f.cache_info()}")
    