from dataclasses import dataclass
from typing import List, Optional
# import re


def compare_ranges(range1: range, range2: range) -> (Optional[range], Optional[List[range]]):
    if range1.stop <= range2.stop and range1.stop > range2.start: #ensure a right overlap or 1 in 2
        if range1.start >= range2.start: # 1 in 2
                overlap = range1
                remainder = None
        else: #right overlap
            overlap = range(range2.start, range1.stop)
            remainder = [range(range1.start, range2.start)]
    elif range1.start >= range2.start and range1.start < range2.stop: #ensure a left overlap or 1 in 2
            if range1.stop < range2.stop: #1 in 2
                overlap = range1
                remainder = None
            else:
                overlap = range(range1.start, range2.stop)
                remainder = [range(range2.stop, range1.stop)]
    elif range1.start < range2.start and range1.stop > range2.stop: # 2 in 1
        overlap = range2
        remainder = [range(range1.start, range2.start), range(range2.stop, range1.stop)]
    else:
        overlap = None
        remainder = None
    # print("range1:", range1, "range2:", range2, "overlap:", overlap, "remainder:", remainder)
    return overlap, remainder

@dataclass
class Mapping:
    dest_range: range
    origin_range: range

    @staticmethod
    def create_mapping(mapping_array: List[int]):
        return Mapping(dest_range=range(mapping_array[0], mapping_array[0]+mapping_array[2]),
                       origin_range = range(mapping_array[1], mapping_array[1]+mapping_array[2]))
    

@dataclass
class Map:
    origin: str
    destination: str
    mappings: List[Mapping]

    @staticmethod
    def import_map(raw_map: str):
        raw_map = raw_map.split("\n")
        title = raw_map.pop(0).replace(" map:", "")
        origin, destination = title.split("-to-")
        mappings = [Mapping.create_mapping([int(n) for n in line.split(" ")]) for line in raw_map]
        
        return Map(origin, destination, mappings)

    def get_dest_single(self, orig_value) -> int:
        for mapping in self.mappings:
            if orig_value in mapping.origin_range:
                index = mapping.origin_range.index(orig_value)
                return mapping.dest_range.__getitem__(index)
        else:
            return orig_value
    
    def get_dest_range(self, orig_ranges: List[range]) -> List[range]:
        remainders = orig_ranges
        destinations = list()
        while remainders != []:
            dests = list()
            current_range = remainders.pop(0)
            for mapping in self.mappings:
                overlap, remainder = compare_ranges(current_range, mapping.origin_range)
                if overlap is not None:
                    overlap: range
                    dest_start_i = mapping.origin_range.index(overlap[0])
                    dest_stop_i = mapping.origin_range.index(overlap[-1])
                    dest_range = mapping.dest_range[dest_start_i:dest_stop_i+1]
                    dests.append(dest_range)
                    if remainder:
                        remainder: List[range]
                        remainders.extend(remainder)
                    break
                else:
                    continue
            if dests == []:
                dests = [current_range]
            destinations.extend(dests)
        
        return destinations
            

def parse_input(fn: str = "5/input.txt") -> (List[int], List[Map]):
    with open(fn, 'r') as f:
        dat = f.read()
    dat = dat.split("\n\n")
    seeds = dat[0].replace("seeds: ", "")
    seeds = [int(seed) for seed in seeds.split(" ")]
    raw_maps = dat[1:]
    good_maps = [Map.import_map(raw_map) for raw_map in raw_maps]
    return seeds, good_maps

def go_through_maps_single(instruction_cursor: int, maps: List[Map]) -> int:
    for map in maps:
        instruction_cursor = map.get_dest_single(instruction_cursor)
    return instruction_cursor

def go_through_maps_range(current_ranges: List[range], maps: List[Map]) -> List[range]:
    for map in maps:
        # print(map.origin, "\n", current_ranges, " -> ", "\n")
        current_ranges = map.get_dest_range(current_ranges)
        # print(map.destination, "\n", current_ranges, "\n")
    return current_ranges

def seeds_part_two(seeds: List[int]) -> List[range]:
    seeds = [range(seeds[i], seeds[i]+seeds[i+1]) for i in range(0, len(seeds), 2)]
    return seeds


def main():
    seeds, maps = parse_input()
    locations = [go_through_maps_single(seed, maps) for seed in seeds]
    print("Part One result:", min(locations))
    seeds_ranges = seeds_part_two(seeds)
    locations = go_through_maps_range(seeds_ranges, maps)
    lowest = min([loc.start for loc in locations])
    print("Part Two result:", lowest)

if __name__ == "__main__":
    main()
    