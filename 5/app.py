from dataclasses import dataclass
from typing import List, Optional
# import re

@dataclass
class Mapping:
    dest_range_start: int
    origin_range_start: int
    range_len: int

    @staticmethod
    def create_mapping(mapping_array: List[int]):
        return Mapping(dest_range_start=mapping_array[0], 
                       origin_range_start=mapping_array[1], 
                       range_len=mapping_array[2])
    
    def create_mapping_dict(self) -> dict:
        origin_range = list(range(self.origin_range_start, self.origin_range_start+self.range_len))
        dest_range = list(range(self.dest_range_start, self.dest_range_start+self.range_len))
        return {origin_n:dest_range[i] for i, origin_n in enumerate(origin_range)}

    

@dataclass
class Map:
    origin: str
    destination: str
    mappings_dict: dict

    @staticmethod
    def import_map(raw_map: str):
        raw_map = raw_map.split("\n")
        title = raw_map.pop(0).replace(" map:", "")
        origin, destination = title.split("-to-")
        mappings = [Mapping.create_mapping([int(n) for n in line.split(" ")]) for line in raw_map]
        mappings_dict = { k:v for mapping in mappings for k, v in mapping.create_mapping_dict().items() }
        
        return Map(origin, destination, mappings_dict)

    def get_dest(self, orig_value) -> int:
        if orig_value in self.mappings_dict:
                return self.mappings_dict[orig_value]
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


def parse_input(fn: str = "5/input.txt") -> (List[int], List[Map]):
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