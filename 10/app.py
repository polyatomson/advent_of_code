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
            ".":Pipe(north=False, south=False, west=False, east=False, name="."),
            "S":Pipe(north=True, south=True, west=True, east=True, name="start")
        }
        return pipe_dict[character]


@dataclass
class Move:
    angle: int
    length: int
    
@dataclass
class Loop:
    moves: List[Move]

    def delete_nonsteps(self):
        self.moves = [move for move in self.moves if move.length !=0]
        print(self.moves)

    def compress_moves(self):
        for i in range(len(self.moves)-2):
            if self.moves[i].angle == self.moves[i+1].angle:
                self.moves[i+1].length += self.moves[i].length
                self.moves[i].length = 0
        
        self.delete_nonsteps()
        print(self.moves)
    
    def draw_loop(self, start: tuple[int, int]=(0, 0), col: str="red"):
        turtle.width(7)
        turtle.penup()
        turtle.goto(start[1]*10, start[0]*10)
        turtle.pendown()
        turtle.color(col)
        for step in self.moves:
            turtle.setheading(0)
            turtle.right(step.angle)
            turtle.forward(step.length*10)
    
    def reduce_loop(self):
        non_negative = lambda x: 1 if x < 0 else x
        for i, move in enumerate(self.moves):
            new_length = non_negative(move.length - 2)
            self.moves[i].length = new_length
        self.delete_nonsteps()
        print(self.moves)
    

@dataclass
class Map:
    map: List[List[Pipe]]
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
    
    def get_pipe(self, coord: tuple[int]) -> Pipe:
        return self.map[coord[0]][coord[1]]

    def step(self, last_move: Move, y_coordinate: int=0, x_coordinate: int=0) -> tuple[Move, (int, int)]:
        start: Pipe = self.map[y_coordinate][x_coordinate]
        if start is None:
            return None #stuck
        all_possible = list()
        
        if start.east:
            try:
                next = self.map[y_coordinate][x_coordinate+1]
                if next.west:
                    if last_move.angle != 180:
                        coor = (y_coordinate, x_coordinate+1)
                        if next.name in ["L", "F", "7", "J", "S"]:
                            corner = coor
                        else:
                            corner = None
                        return Move(0, 1), coor, corner
            except Exception as ex:
                # print(ex)
                False
        if start.west:
            try:
                next = self.map[y_coordinate][x_coordinate-1]
                if next.east:
                    if last_move.angle != 0:
                        coor = (y_coordinate, x_coordinate-1)
                        if next.name in ["L", "F", "7", "J", "S"]:
                            corner = coor
                        else:
                            corner = None
                        return Move(180, 1), coor, corner
            except:
                False
        if start.north:
            try:
                next = self.map[y_coordinate-1][x_coordinate]
                if next.south:
                    if last_move.angle != 90:
                        coor = (y_coordinate-1, x_coordinate)
                        if next.name in ["L", "F", "7", "J", "S"]:
                            corner = coor
                        else:
                            corner = None
                        return Move(270, 1), coor, corner
                        
            except:
                False
        
        if start.south:
            try:
                next = self.map[y_coordinate+1][x_coordinate]
                if next.north:
                    if last_move.angle != 270:
                        coor = (y_coordinate+1, x_coordinate)
                        if next.name in ["L", "F", "7", "J", "S"]:
                            corner = coor
                        else:
                            corner = None
                        return Move(90, 1), coor, corner
            except:
                False

        
        return None # stuck
    
    

    def go_through(self) -> tuple[List[tuple[int]], Loop]:
        start = self.step(Move(7, 1), self.start_y, self.start_x)
        last_move, next_coors, corner = start
        loop = [(self.start_y, self.start_x), next_coors]
        corners = [(self.start_y, self.start_x), corner]
        moves = [last_move]
        
        while next_coors != (self.start_y, self.start_x):
            new_step = self.step(last_move, next_coors[0], next_coors[1])
            if new_step is not None:
                last_move, next_coors, corner = new_step
                moves.append(last_move)
                loop.append(next_coors)
                corners.append(corner)
                next_name = self.get_pipe(next_coors).name
                print(next_name, end="->")
            else:
                print("stuck")
                break
        print("\n")
        corners = [corner for corner in corners if corner is not None]
        return loop, Loop(moves), corners
        
    
    
def area(loop: List[tuple[int,int]], corners: List[tuple[int,int]]):
        corners.append(loop[0])
        area = [(corners[i][1] * corners[i+1][0]) - (corners[i][0] * corners[i+1][1]) for i in range(0, len(corners)-1)]
        area = abs(sum(area))/2
        inside = area - (len(loop)-1)/2 + 1
        return int(inside)
        
                
                    



def import_dat(fn: str="10/input.txt"):
    with open(fn, 'r') as f:
        dat = f.readlines()
    lines = [line.strip("\n") for line in dat]
    return lines

def main():
    lines = import_dat()
    map = Map.import_pipes(lines)
    loop, moves, corners = map.go_through()
    furthest = len(moves.moves)//2
    print("Part One result:", furthest)
    moves.compress_moves()
    print("Part One result:", furthest)
    inner_tiles = area(loop, corners)
    print("Part Two result:", inner_tiles)


if __name__ == "__main__":
    main()