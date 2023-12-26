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
    
    def turn_north_from_west(self):
        cols = [''.join([row[i] for row in self.rows]) for i in range(len(self.rows[0]))]
        self.rows = cols
        self.left_headed = 'north'
    
    def turn_west_from_north(self):
        cols = [''.join([row[i] for row in self.rows]) for i in range(len(self.rows[0]))]
        self.rows = cols
        self.left_headed = 'west'
    
    def turn_south_from_west(self):
        self.turn_north_from_west()
        self.rows = list(reversed(self.rows))
        self.left_headed = 'south'
    
    def turn_east_from_south(self):
        self.turn_west_from_north()
        self.left_headed = 'east'
    
    def turn_north_from_east(self):
        self.turn_south_from_west()
        self.left_headed = 'north'
    
    @staticmethod
    def cut_row_into_blocks(row: str):
        blockings = re.finditer('#+', row)
        blockings = [match_obj for match_obj in blockings]
        if blockings == []:
            return [row]
        blocks = [row[0:blockings[0].start()]]
        for x, blocking in enumerate(blockings):
            if x < len(blockings)-1:
                start, stop = blocking.start(), blocking.end()
                blocks.append(row[start:stop])
                blocks.append(row[stop:blockings[x+1].start()])
        blocks.append(row[blockings[-1].start():blockings[-1].end()])
        blocks.append(row[blockings[-1].end():])
        blocks = [block for block in blocks if block != '']
        return blocks


    def tilt_left(self):
        for i, row in enumerate(self.rows):
            blocks = Board.cut_row_into_blocks(row)
            # blocks = [block for sublist in blocks for block in sublist]
            
            # spaces = row.split('#')
            # tilted_line = []
            for c, block in enumerate(blocks):
                if '#' not in block:
                    space_len = len(block)
                    n_rocks = sum([1 for char in block if char == 'O'])
                    n_empty = space_len-n_rocks
                    tilted_space = 'O'*n_rocks + '.'*n_empty
                    blocks[c] = tilted_space

                # tilted_line.append(tilted_space)
            self.rows[i] = ''.join(blocks)
    
    def total_load(self) -> int:
        res = 0
        for i, line in enumerate(reversed(self.rows)):
            ows = [1 for char in line if char == 'O']
            res += sum(ows) * (i+1)
        return res
    

    def cycle(self):
        if self.left_headed != 'north':
            raise Exception("headed the wrong direction")
        self.tilt_left()
        self.turn_west_from_north()
        self.tilt_left()
        self.turn_south_from_west()
        self.tilt_left()
        self.turn_east_from_south()
        self.tilt_left()
        self.turn_north_from_east()
    
def main():
    # Part One
    board = Board.load()
    print(board)
    board.turn_north_from_west()
    board.tilt_left()
    board.turn_west_from_north()
    print(board)
    print("Part one result:", board.total_load())

    # Part Two
    board = Board.load()
    board.turn_north_from_west()
    for n in range(1000000000):
        board.cycle()
    print("Part two result:", board.total_load())

if __name__ == '__main__':
    main()