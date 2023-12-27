from typing import List
from dataclasses import dataclass

def find_pattern(sequence: List[int]):
    n_steps = None

    for i, n in enumerate(sequence):
        if n_steps is not None:
            break
        rest_of_sequence = sequence[i+1:]
        if n in rest_of_sequence:
            next_occurences = [pos for pos, num in enumerate(rest_of_sequence) if num == n]
        else:
            continue
        for next_occ_i in next_occurences:
            for x in range(1, len(rest_of_sequence)-1-next_occ_i):
                if sequence[i+x] != rest_of_sequence[next_occ_i+x]:
                    in_pattern=False
                    break
                else:
                    in_pattern=True
                    continue
            if in_pattern is True:
                start_pattern = i
                n_steps = next_occ_i
                break
    try:
        n_before_loop = start_pattern
        pattern = sequence[start_pattern:start_pattern+n_steps+1]
        return n_before_loop, pattern
    except:
        raise Exception("Trying a larger number of cycles")

@dataclass
class Board:
    rows: List[str]
    left_headed: str = 'west'

    def __repr__(self) -> str:
        if_k_left_then_above_v = {'west': 'north', 'north': 'east', 
                                  'south': 'west', 'east': 'south'}
        above = if_k_left_then_above_v[self.left_headed]
        return above + '\n' + ('\n'.join(self.rows)) + '\n'

    @staticmethod
    def load(fn: str='14/input_test.txt') -> 'Board':
        with open(fn, 'r') as f:
            dat = f.readlines()
        dat = [line.strip('\n') for line in dat]
        return Board(dat)
    
    def turn_right(self):

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
    

def part_one(fn: str='14/input_test.txt'):
    board = Board.load(fn)
    print(board)
    board.turn_left() # north left
    board.tilt_left()
    board.turn_right() # compare results
    print(board)
    
    return board.total_load()

def part_two(n_cycles: int, fn: str='14/input_test.txt', more_cycles: int=50):
    board = Board.load(fn)
    board.turn_left() # north left
    
    not_enough = True
    loads = []
    #test algorithm on n cycles to find a pattern
    while not_enough is not False:
        for cikl in range(more_cycles):
            board.cycle()
            board.turn_right()
            load = board.total_load()
            board.turn_left()
            loads.append(load)
        try:
            #find a pattern
            n_before_loop, pattern = find_pattern(loads)
            not_enough = False
        except Exception as ex:
            print(ex)
            continue
    
    # find where in the cycle it would stop
    cycle_leftover = (n_cycles - n_before_loop)%len(pattern)
    final_load = pattern[cycle_leftover-1]

    return final_load


def main():
    # Part One
    final_load = part_one()
    print("Part one result:", final_load)
    # Part Two
    final_load = part_two(1000**3, '14/input.txt')
    print("Part two result:", final_load)
    

if __name__ == '__main__':
    main()