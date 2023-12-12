from dataclasses import dataclass
from typing import List, Union, Optional
from collections import Counter
import turtle

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
        return Map(map, y_size=y_dim, x_size=x_dim, start_y=start_y, start_x=start_x)
    
    
    def draw_loop(self, loop: List[tuple[int]]):
        turtle.color("black")
        field_x = range(0, self.x_size+1)
        field_y = range(-(self.y_size-1), 2)
        for x in field_x:
            turtle.penup()
            turtle.setposition(x*10-5, 5)
            turtle.pendown()
            turtle.goto(x*10-5, -(self.y_size-1)*10-5)

        for y in field_y:
            turtle.penup()
            turtle.setposition(-5, (y*10)-5)
            turtle.pendown()
            turtle.goto((self.x_size)*10-5, (y*10)-5)

        turtle.penup()
        turtle.setposition((loop[0][1]*10, -loop[0][0]*10))
        turtle.pendown()
        turtle.color("red")
        turtle.width(9)
        for coor in loop[1:]:
            x = coor[1]
            y = -coor[0]
            turtle.goto((x*10, y*10))
            # print(turtle.pos())
        turtle.goto((loop[0][1]*10, -loop[0][0]*10))
        turtle.mainloop()


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

    def find_within_loop(self, borders: List[tuple[int]]):
        not_borders = [(y, x) for y in range(self.y_size) 
                       for x in range(self.x_size) 
                       if (y, x) not in borders]
        out = list()
        
        y_lines = [
            [not_border for not_border in not_borders 
                 if not_border[0] == y ]
                 for y in range(self.y_size)]
        #remove outer lines:
        y_first_and_last_line = [y_lines.pop(i)
                                 for i in [0, -1]]
        out.extend(y_first_and_last_line)

        #remove the lines without any loop pipes
        y_lines_empty = [y_lines.pop(y_line_id) for y_line_id, y_line
                          in enumerate(y_lines) if len(y_line) == self.x_size]
        out.extend(y_lines_empty)
                
        x_lines = [
            [not_border for not_border in not_borders 
                 if not_border[1] == x ]
                 for x in range(self.x_size)]
        #remove the outer columns
        x_first_and_last_line = [x_lines.pop(i)
                                 for i in [0, -1]]
        out.extend(x_first_and_last_line)

        #remove the columns without any loop pipes
        x_lines_empty = [x_lines.pop(x_line_id) for x_line_id, x_line
                          in enumerate(x_lines) if len(x_line) == self.y_size]
        out.extend(x_lines_empty)
        
        flatten = lambda my_list: [item for sublist in my_list for item in sublist] if my_list != [] else []
        out = flatten(out)
        
        out = [key for key in Counter(out)] #removes the duplicates
        out = sorted(out)
        # for i, tile in enumerate(not_borders):
        #     tile_out = tile[0] in [0, self.y_size-1] or tile[1] in [0, self.y_size] or tile in out
        #     if :
        #         out.append(not_borders[i])
        potentially_in = [tile for tile in not_borders if tile not in out]
        for tile in potentially_in:
            if 
        return 0


def import_dat(fn: str="10/input_test.txt"):
    with open(fn, 'r') as f:
        dat = f.readlines()
    lines = [line.strip("\n") for line in dat]
    return lines

def main():
    lines = import_dat()
    map = Map.import_pipes(lines)
    loop, furthest = map.go_through()
    # map.draw_loop(loop)
    print("Part One result:", furthest)
    n_tiles_inside = map.find_within_loop(loop)
    print("Part Two result:", n_tiles_inside)


if __name__ == "__main__":
    main()