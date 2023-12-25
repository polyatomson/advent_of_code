import re
from dataclasses import dataclass
from typing import List, Optional
import itertools



@dataclass
class SpringLine:
    raw_line: str
    error_chunk_lengths: List[int]


    @staticmethod
    def load(raw_springs: str, raw_errors: str) -> 'SpringLine':
        error_chunk_lengths = [int(x) for x in raw_errors.strip("\n").split(",")]
        return SpringLine(raw_springs, error_chunk_lengths)
    
    def evaluate_options(self):
        regexes = []

        for error_length in self.error_chunk_lengths:
            repetitions = str(error_length)
            regex = r"#{" + repetitions + r"}?"
            regexes.append(regex)

        regex = r"\.+".join(regexes)
        regex = r"\.*" + regex + r"\.*"
        
        questions = [ques.start() for ques in re.finditer('\?', self.raw_line)]
        
        combs = itertools.product('.#', repeat=len(questions))        
        n_options = 0

        for comb in combs:
            line = list(self.raw_line)
            for i, ques in enumerate(questions):
                line[ques] = comb[i]
            test_line = ''.join(line)
            found_match = re.fullmatch(regex, test_line)
            if found_match is not None:
                n_options += 1

        return n_options


def import_data(fn: str="12/input_test.txt") -> List[SpringLine]:
    with open(fn, 'r') as f:
        dat = f.readlines()
    dat = [line.split(" ") for line in dat]
    return [SpringLine.load(row[0], row[1]) for row in dat]

def main():
    dat = import_data('12/input.txt')
    options = 0
    for x in dat:
        options += x.evaluate_options()
    print("Part One Result:", options)

if __name__ == '__main__':
    main()

# def rangify(int_list: List[int]):
#     if int_list == []:
#         return []
#     cut = [[int_list[0]]]
#     for i, n in enumerate(int_list[1:]):
#         if n - int_list[i] == 1:
#             cut[-1].append(n)
#         else:
#             cut.append([n])
    
#     rangified = [range(min(l), max(l)+1) for l in cut]
#     return rangified

# def compress_ranges(r_list: List[range]):
#     compressed = list()
#     for i, r in enumerate(r_list[1:]):
#         if r_list[i].stop == r.start:
#             if compressed != []:
#                 compressed[-1] = range(compressed[-1].start, r.stop)
#             else:
#                 compressed.append(range(r_list[i].start, r.stop))
#         else:
#             if compressed != []:
#                 compressed.append(r)
#             else:
#                 compressed.extend([r_list[i], r])
#     return compressed

# def rangified_len(rangified: List[range]) -> int:
#     return sum([len(r) for r in rangified])