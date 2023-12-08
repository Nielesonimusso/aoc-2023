from functools import reduce
from itertools import batched, chain
from collections.abc import Iterator, Iterable

class RangeMapping:
    def __init__(self, destination_start, source_start, length):
        self.source_range = range(source_start, source_start + length)
        self.destination_offset = destination_start - source_start
    
    def split_range(self, range_: range) -> tuple[list[range], list[range]]:
        if range_.start < self.source_range.start:
            if range_.stop <= self.source_range.start:
                return ([], [range_])
            elif range_.stop < self.source_range.stop:
                return ([range(self.source_range.start, range_.stop)],
                        [range(range_.start, self.source_range.start)])
            else:
                return ([self.source_range],
                        [range(range_.start, self.source_range.start),
                         range(self.source_range.stop, range_.stop)]) 
        elif range_.start < self.source_range.stop:
            if range_.stop <= self.source_range.stop:
                return ([range_], [])
            else:
                return ([range(range_.start, self.source_range.stop)], 
                        [range(self.source_range.stop, range_.stop)])
        else:
            return ([], [range_])
        
    def _offset_range(self, range_: range) -> range:
        return range(range_.start + self.destination_offset, 
                     range_.stop + self.destination_offset)
    
    def _apply_single(self, range_: range) -> tuple[list[range], list[range]]:
        split_ranges = self.split_range(range_)
        return ([*map(lambda r: self._offset_range(r), split_ranges[0])], 
                split_ranges[1])
            
    def apply(self, ranges: tuple[list[range], list[range]]) -> tuple[list[range], list[range]]:
        applied_map = [*map(self._apply_single, ranges[1])]
        completed_map = map(lambda a: a[0], applied_map)
        remaining_map = map(lambda a: a[1], applied_map)
        result = ([*chain(ranges[0], *completed_map)], [*chain(*remaining_map)])
        return result
    
class Map:
    def __init__(self, name: str):
        self.name = name
        self.range_mappings = list()

    def add_range_mapping(self, range_mapping: RangeMapping):
        self.range_mappings.append(range_mapping)

    def apply(self, ranges: list[range]) -> list[range]:
        print(f"applying map {self.name}")
        return [*chain(*reduce(lambda r, rm: rm.apply(r), self.range_mappings, ([], ranges)))]

class Almanac:
    def __init__(self):
        self.maps = list()

    def add_map(self, map: Map):
        self.maps.append(map)

    def apply(self, ranges: list[range]) -> int:
        final_ranges = reduce(lambda ir, m: m.apply(ir), self.maps, ranges)
        return reduce(min, [r.start for r in final_ranges])

almanac = Almanac()

with open("data.txt", "r") as file:
    value_ranges: list[range] = [range(int(s), int(s) + int(l)) for s, l in batched(file.readline().split(" ")[1:], 2)]
    print(f"starting ranges: {value_ranges}")
    print(f"total length: {sum(len(r) for r in value_ranges)}")

    # fill the ALMANAC
    current_map: None | Map = None
    for line in file:
        # skip empty line
        if len(line.strip()) == 0:
            continue

        # start a new mapping when the line says "map"
        if 'map' in line:
            if current_map is not None:
                almanac.add_map(current_map)
            current_map = Map(line.strip())
            print(f"Adding {line}")
            continue

        current_map.add_range_mapping(
            RangeMapping(*[int(p.strip()) for p in line.split(" ")]))
    # the last current_map should still be added to the ALMANAC
    almanac.add_map(current_map)

    # apply the ALMANAC to ALL our value ranges, and reduce to the minimum
    lowest_location = almanac.apply(value_ranges)
    print(lowest_location)