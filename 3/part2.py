from part1 import get_spans, compare_two_spans
from typing import List, Tuple, Dict



def check_for_gears(astrixes: List[Tuple[int]], numbers: List[Dict]) -> List[List[int]]:
    gear_groups = list()
    for i, line in enumerate(astrixes):
        if line == []:
            continue
        else:
            if i == 0:
                vicinity_numbers = [ number for line in numbers[i:i+2] for number in line]
            elif i == len(astrixes)-1:
                vicinity_numbers = [ number for line in numbers[i-1:i+1] for number in line]
            else:
                vicinity_numbers = [ number for line in numbers[i-1:i+2] for number in line]
            
            for ast in line:
                adjacent_numbers = []
                for number in vicinity_numbers:
                    adjacency = compare_two_spans(ast, number["span"])
                    if adjacency is True:
                        adjacent_numbers.append(int(number["number"]))
                if len(adjacent_numbers) == 2:
                    # It's a gear!
                    gear_groups.append(adjacent_numbers)
    return gear_groups


def multiply(ints: List[int]) -> int:
    res = 1
    while len(ints) > 0:
        res = res * ints.pop()
    return res


def main():

    with open('3/input_test.txt', 'r') as fn:
        dat = fn.readlines()

    dat = [line.strip("\n") for line in dat]
    numbers, characters = get_spans(dat)
    astrixes = [[char["span"] for char in line if char["char"] == "*"] for line in characters ]
    gear_pairs = check_for_gears(astrixes, numbers)
    gear_ratios = [multiply(gear_pair) for gear_pair in gear_pairs]

    print("result:", sum(gear_ratios))


if __name__ == '__main__':
    main()