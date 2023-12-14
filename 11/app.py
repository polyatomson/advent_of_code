# from numpy import matrix
from __future__ import annotations
from dataclasses import dataclass
from typing import List


@dataclass
class Matrix:
    matrix: List[List[int]]
    x_len: int
    y_len: int
    
    @staticmethod
    def import_matrix(fn: str="11/input_test.txt") -> Matrix:
        with open(fn) as f:
            dat = f.readlines()
        dat = [list(line.strip("\n")) for line in dat]
        digitalize = lambda x: 0 if x=="." else 1
        dat = [[digitalize(letter) for letter in line] for line in dat]
        
        return Matrix(dat, len(dat[0]), len(dat))

    def get_item(self, coor_x: int, coor_y: int) -> int:
        return self.matrix[coor_y][coor_x]

    def transpose(self) -> None:
        transposed = list()
        for x in range(self.x_len):
            transposed.append([])
            for y in range(self.y_len):
                transposed[-1].append(self.get_item(x, y))
        self.matrix = transposed
        
        self.x_len = len(self.matrix[0])
        self.y_len = len(self.matrix)
    
    def expand_galaxies_vertically(self, n: int) -> None:
        for i, line in enumerate(self.matrix):
            if 1 not in line:
                 self.matrix[i] = [n for x in line]
    
    def expand_galaxies(self, n: int) -> None:
        self.expand_galaxies_vertically(n)
        self.transpose()
        self.expand_galaxies_vertically(n)
        self.transpose()
    
    def find_ones(self) -> List[tuple[int, int]]:
        coors = [(x, y) for y in range(self.y_len) 
                 for x in range(self.x_len)
                 if self.get_item(x, y) == 1]
        return coors
    
    def find_path(self, galaxy1: tuple[int, int], galaxy2: tuple[int, int]) -> int:
        x1, y1 = galaxy1
        x2, y2 = galaxy2
        if x1 < x2:
            path_x = range(x1+1, x2+1)
        else:
            path_x = range(x2, x1)
        if y1 <= y2:
            path_y = range(y1, y2)
        # else:
        #     path_y = range(y2, y1)
        unnull = lambda x: x if x != 0 else 1
        path_x_values = [unnull(self.get_item(x, y1)) for x in path_x]
        path_y_values = [unnull(self.get_item(x2, y)) for y in path_y]
        steps = sum(path_x_values) + sum(path_y_values)

        return steps
    
    
    def find_all_paths(self, ones, part_two: bool=False):
        i = 0
        result = 0
        while len(ones) > 1:
            current = ones.pop(i)
            for one in ones:
                result += self.find_path(current, one)
        return result



def main():
    galaxies = Matrix.import_matrix(fn="11/input.txt")
    galaxies.expand_galaxies(n=2)
    ones = galaxies.find_ones()
    result1 = galaxies.find_all_paths(ones)
    print("Part One", result1)

    galaxies = Matrix.import_matrix(fn="11/input.txt")
    galaxies.expand_galaxies(n=10**6)
    ones = galaxies.find_ones()
    result2 = galaxies.find_all_paths(ones, part_two=True)
    print("Part Two", result2)



if __name__ == "__main__":
    main()
