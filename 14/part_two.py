from typing import List
from dataclasses import dataclass
import re

@dataclass
class Board:
    rows: List[str]
    left_headed: str = 'west'

    def __repr__(self) -> str:
        return self.left_headed + '\n' + ('\n'.join(self.rows)) + '\n'

    @staticmethod
    def load(fn: str='14/input_test.txt') -> 'Board':
        with open(fn, 'r') as f:
            dat = f.readlines()
        dat = [line.strip('\n') for line in dat]
        return Board(dat)
    
    def turn_right(self):
        # for i in range(len(self.rows[0])):
        #     for row in reversed(self.rows):
        #         row[i]

        cols = [''.join([row[i] for row in reversed(self.rows)]) for i in range(len(self.rows[0]))]
        self.rows = cols
        if self.left_headed == 'north':
            self.left_headed = 'west'
        elif self.left_headed == 'west':
            self.left_headed = 'south'
        elif self.left_headed == 'south':
            self.left_headed = 'east'
        elif self.left_headed == 'east':
            self.left_headed = 'north'
    
    def turn_left(self):
        cols = [''.join([row[i] for row in self.rows]) for i in reversed(range(len(self.rows[0])))]
        self.rows = cols
        if self.left_headed == 'west':
            self.left_headed = 'north'
        else:
            raise Exception('dubious rotation')
    
    # def turn_south_from_west(self):
    #     self.turn_north_from_west()
    #     self.rows = list(reversed(self.rows))
    #     self.left_headed = 'south'
    
    # def turn_east_from_south(self):
    #     self.turn_north_from_west()
    #     self.rows = list(reversed(self.rows))
    #     self.left_headed = 'east'
    
    # def turn_north_from_east(self):
    #     self.turn_south_from_west()
    #     self.left_headed = 'north'
    
    @staticmethod
    def cut_row_into_blocks(row: str):
        blocks = row.split('#')
        return blocks


    def tilt_left(self):
        for i, row in enumerate(self.rows):
            blocks = Board.cut_row_into_blocks(row)
            # blocks = [block for sublist in blocks for block in sublist]
            
            # spaces = row.split('#')
            # tilted_line = []
            for c, block in enumerate(blocks):
                if '#' not in block and block !='':
                    space_len = len(block)
                    n_rocks = sum([1 for char in block if char == 'O'])
                    n_empty = space_len-n_rocks
                    tilted_space = 'O'*n_rocks + '.'*n_empty
                    blocks[c] = tilted_space

                # tilted_line.append(tilted_space)
            self.rows[i] = '#'.join(blocks)
    
    def total_load(self) -> int:
        if self.left_headed != 'west':
            raise Exception('turn the west side left to get the northern load')
        res = 0
        for i, line in enumerate(reversed(self.rows)):
            ows = [1 for char in line if char == 'O']
            res += sum(ows) * (i+1)
        return res
    

    def cycle(self):
        if self.left_headed != 'north':
            raise Exception("headed the wrong direction")
        self.tilt_left()
        self.turn_right() #west left
        self.tilt_left() 
        self.turn_right() #south left
        self.tilt_left()
        self.turn_right() #east left
        self.tilt_left()
        
        self.turn_right() # north left again
    
    
def main():
    # Part One
    board = Board.load('14/input_test.txt')
    print(board)
    board.turn_left() # north left
    print(board)
    board.tilt_left()
    print(board)
    board.turn_right() # compare results
    print(board)
    print("Part one result:", board.total_load())

    # Part Two
    board = Board.load('14/input_test.txt')
    print(board)
    board.turn_left() # north left
    # print(board)
    # inp = ''
    n_cycles = 0
    loads = []
    # while load != 64:
    while n_cycles < 200:
        # inp = input("continue?")
        n_cycles += 1
        board.cycle()
        board.turn_right()
        print(n_cycles, board)
        load = board.total_load()
        board.turn_left()
        # if load in loads:
        #     print("been_there!")
        # else:
        #     print("new")
        loads.append(load)
    


    print("Part two result:", board.total_load())

if __name__ == '__main__':
    main()