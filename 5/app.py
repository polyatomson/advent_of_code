from dataclasses import dataclass
from typing import List, Optional
# import re

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

    def get_dest(self, orig_value) -> int:
        for mapping in self.mappings:
            if orig_value in mapping.origin_range:
                index = mapping.origin_range.index(orig_value)
                return mapping.dest_range.__getitem__(index)
        else:
            return orig_value

# @dataclass
# class SeedInstructions:
#     seed: int
#     soil: Optional[int]
#     fertilizer: Optional[int]
#     water: Optional[int]
#     light: Optional[int]
#     temperature: Optional[int]
#     humidity: Optional[int]
#     location: Optional[int]


def parse_input(fn: str = "5/input_test.txt") -> (List[int], List[Map]):
    with open(fn, 'r') as f:
        dat = f.read()
    dat = dat.split("\n\n")
    seeds = dat[0].replace("seeds: ", "")
    seeds = [int(seed) for seed in seeds.split(" ")]
    raw_maps = dat[1:]
    good_maps = [Map.import_map(raw_map) for raw_map in raw_maps]
    return seeds, good_maps

def go_through_maps(instruction_cursor: int, maps: List[Map]):
    for map in maps:
        instruction_cursor = map.get_dest(instruction_cursor)
    return instruction_cursor


def main():
    seeds, maps = parse_input()
    locations = [go_through_maps(seed, maps) for seed in seeds]
    print("Part One result:", min(locations))

if __name__ == "__main__":
    main()