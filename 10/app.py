from dataclasses import dataclass
from typing import List, Union, Optional
@dataclass
class Pipe:
    north: bool
    south: bool
    west: bool
    east: bool
    name: str

    @staticmethod
    def import_pipe(character: str):
        pipe_dict = {
            "|":Pipe(north=True, south=True, west=False, east=False, name="|"),
            "-":Pipe(north=False, south=False, west=True, east=True, name="-"),
            "L":Pipe(north=True, south=False, west=False, east=True, name="L"),
            "J":Pipe(north=True, south=False, west=True, east=False, name="J"),
            "7":Pipe(north=False, south=True, west=True, east=False, name="7"),
            "F":Pipe(north=False, south=True, west=False, east=True, name="F"),
            ".":None,
            "S":Pipe(north=True, south=True, west=True, east=True, name="start")
        }
        return pipe_dict[character]
    
    # def possible_directions(self):


@dataclass
class Map:
    map: List[List[Union[None, str]]]
    y_size: int
    x_size: int
    start_y: int
    start_x: int

    @staticmethod
    def import_pipes(lines: List[str]):
        y_dim = len(lines)
        x_dim = len(lines[0])
        map = list()
        for line in lines:
            characters = list(line)
            pipes = [Pipe.import_pipe(character) for character in characters]
            map.append(pipes)
            if "S" in characters:
                start_x = characters.index("S")
                start_y = lines.index(line)
        return Map(map, y_dim, x_dim, start_y, start_x)
    
    def step(self, y_coordinate: int=0, x_coordinate: int=0):
        start: Pipe = self.map[y_coordinate][x_coordinate]
        if start is None:
            return None #stuck
        all_possible = list()
        
        if start.east:
            try:
                next = self.map[y_coordinate][x_coordinate+1]
                if next.west:
                    all_possible.append((next, y_coordinate, x_coordinate+1))
            except:
                False
        if start.west:
            try:
                next = self.map[y_coordinate][x_coordinate-1]
                if next.east:
                    all_possible.append((next, y_coordinate, x_coordinate-1))
            except:
                False
        if start.north:
            try:
                next = self.map[y_coordinate-1][x_coordinate]
                if next.south:
                    all_possible.append((next, y_coordinate-1, x_coordinate))
            except:
                False
        if start.south:
            try:
                next = self.map[y_coordinate+1][x_coordinate]
                if next.north:
                    all_possible.append((next, y_coordinate+1, x_coordinate))
            except:
                False
        
        if all_possible == []:
            return None #stuck
        else:
            return all_possible


    def go_through(self) -> (List[tuple[int]], int):
        start: Pipe = self.map[self.start_y][self.start_x]
        start_options = self.step(self.start_y, self.start_x)
        # start = Pipe(True, True, True, True, "false_start")

        for start_option in start_options[0:1]:
            next, next_y_coor, next_x_coor = start_option
            been_to = [(self.start_y, self.start_x),
                       (next_y_coor, next_x_coor)]
            print("\n\n\n", next.name)
            while next != "finish":
                # print(next.name)
                all_possible = self.step(next_y_coor, next_x_coor)
                stuck = True
                for possible in all_possible:
                    if possible is None:
                        continue
                    next_poss, next_y_coor_poss, next_x_coor_poss = possible
                    if not (next_y_coor_poss, next_x_coor_poss) in been_to:
                        next, next_y_coor, next_x_coor = next_poss, next_y_coor_poss, next_x_coor_poss
                        stuck = False
                        print(next.name, end="->")
                        # continue
                    elif next_poss.name == "start" and len(been_to)>3:
                        next = "finish"
                    else:
                        continue
                if not stuck:
                    been_to.append((next_y_coor, next_x_coor))
                else:
                    if next == "finish":
                        print("finish")
                    else:
                        print("stuck")
                    break
            print(len(been_to))

        # return self.map[furthest_coor_y][furthest_coor_x]
        return been_to, len(been_to)//2
        
    def get_pipe(self, coord: tuple[int]):
        return self.map[coord[0]][coord[1]]

    def find_within_loop(self, been_to: List[tuple[int]]):
        n_inside = 0
        for y_coor in range(self.y_size):
            loop_borders = [border[1] for border in been_to if border[0] == y_coor]
            loop_borders = sorted(loop_borders)
            horizontal = [[]]
            horizontal_ind = 0
            smth_inside = False
            for i in range(1, len(loop_borders)):
                # smth_inside = False
                if loop_borders[i] - loop_borders[i-1] == 1:
                    if loop_borders[i-1] not in horizontal[horizontal_ind]:
                        horizontal[horizontal_ind].extend([loop_borders[i-1], loop_borders[i]])
                    else:
                        horizontal[horizontal_ind].append(loop_borders[i])
                    continue
                    # i loop_
                else:
                    smth_inside = True
                    horizontal.append([])
                    horizontal_ind += 1
                    # usable_borders.append(loop_borders[i-1])
                    # usable_borders.append(loop_borders[i])
            if smth_inside:
                non_lines
                for i in range(1, len(horizontal), 2):
                    if len(horizontal[i-1]) == 1:
                    inside = range(horizontal[i-1][-1], horizontal[i][0]-1)
                    n = len(inside)
                    if n > 0:
                        print(y_coor)
                        print(loop_borders)
                        print("inside:", n)
                    n_inside += len(inside)
            
        return n_inside


def import_dat(fn: str="10/input_test.txt"):
    with open(fn, 'r') as f:
        dat = f.readlines()
    lines = [line.strip("\n") for line in dat]
    return lines

def main():
    lines = import_dat()
    map = Map.import_pipes(lines)
    loop, furthest = map.go_through()
    print("Part One result:", furthest)
    n_tiles_inside = map.find_within_loop(loop)
    print("Part Two result:", n_tiles_inside)


if __name__ == "__main__":
    main()