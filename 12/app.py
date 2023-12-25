import re
from dataclasses import dataclass
from typing import List, Optional

# @dataclass
# class SpringChunk:
#     error: Optional[bool] #True if '#', false if '.', None if unknown
#     n: int

#     @staticmethod
#     def create(chunk: str) -> 'SpringChunk':
#         if '.' in chunk:
#             error = False
#         elif '#' in chunk:
#             error = True
#         else:
#             error = None
#         return SpringChunk(error, len(chunk))

def rangify(int_list: List[int]):
    if int_list == []:
        return []
    cut = [[int_list[0]]]
    for i, n in enumerate(int_list[1:]):
        if n - int_list[i] == 1:
            cut[-1].append(n)
        else:
            cut.append([n])
    
    rangified = [range(min(l), max(l)+1) for l in cut]
    return rangified

def compress_ranges(r_list: List[range]):
    compressed = list()
    for i, r in enumerate(r_list[1:]):
        if r_list[i].stop == r.start:
            if compressed != []:
                compressed[-1] = range(compressed[-1].start, r.stop)
            else:
                compressed.append(range(r_list[i].start, r.stop))
        else:
            if compressed != []:
                compressed.append(r)
            else:
                compressed.extend([r_list[i], r])
    return compressed

def rangified_len(rangified: List[range]) -> int:
    return sum([len(r) for r in rangified])


@dataclass
class SpringLine:
    raw_line: str
    candidates: List[range]
    error_chunk_lengths: List[int]
    n_errors: int
    # '?' info
    n_unknown: int
    unknown_chunks: List[range]
    # '#' info
    n_certain_errors: int
    certain_errors_chunks: List[range]
    # '.' info
    n_valid: int
    valid_chunks: List[range]


    @staticmethod
    def load(raw_springs: str, raw_errors: str) -> 'SpringLine':
        error_chunk_lengths = [int(x) for x in raw_errors.strip("\n").split(",")]
        n_error_chunks = len(error_chunk_lengths)
        n_errors = sum(error_chunk_lengths)
        unknown = [i for i, x in enumerate(raw_springs) if x == "?"]
        n_unknown = len(unknown)
        unknown_chunks = rangify(unknown)
        certain_errors = [i for i, x in enumerate(raw_springs) if x == "#"]
        n_certain_errors = len(certain_errors)
        certain_errors_chunks = rangify(certain_errors)
        valid = [i for i, x in enumerate(raw_springs) if x == "."]
        n_valid = len(valid)
        valid_chunks = rangify(valid)
        all_chunks = certain_errors_chunks + unknown_chunks
        all_chunks = sorted(all_chunks, key=lambda chunk: chunk.start)
        all_chunks = compress_ranges(all_chunks)
        return SpringLine(raw_springs, all_chunks, error_chunk_lengths, n_errors, 
                          n_unknown, unknown_chunks, 
                          n_certain_errors, certain_errors_chunks, 
                          n_valid, valid_chunks)
    
    def evaluate_options(self):
        # certain_errors_chunks_lengths = [len(r) for r in self.certain_errors_chunks]
        # if len(self.candidates) == len(self.error_chunk_lengths):
        regexes = []
        regexes_places = []
        for error_length in self.error_chunk_lengths:
            repetitions = str(error_length)
            # regex = r"(?:(?:\?|#)" + repetitions + r")(?:$|\?)?|(?:(?:^|\?)(?:\?|#)" + repetitions + r")"
            regex_left = r"(?:\.|\?|$)*?((?:\?|#){"
            regex_right = r"})"
            regex = regex_left + repetitions + regex_right
            regexes.append(regex)

            repetitions_max = sum(self.error_chunk_lengths)
            repetitions_range = str(repetitions) + "," + str(repetitions_max)
            regex_left = r"(\.|\?|$)*?((?:\?|#){"
            regex_right = r"})"
            regex = regex_left + repetitions_range + regex_right
            # print(regex_right)
            # print(regex)
            regexes_places.append(regex)
        regex = "(?:\.|\?)+?".join(regexes)
        regex += "(?:\.|\?)*"
        
        found_matches = re.findall(regex, self.raw_line)[0]
        
        regex_places = "(\.|\?)+?".join(regexes_places) + "(\.|\?)*?"
        found_places = re.findall(regex_places, self.raw_line)
        found_places = [x for x in found_places[0] if x != '' and x!='.']
        # for i, span in found_matches:
        #     span_ready = span.replace('?', '#')
        #     if 

        print()
        
        

        
        # for cand in self.candidates:
        #     print(cand, self.raw_line[cand.start:cand.stop])
        #     subline = self.raw_line[cand.start:cand.stop]
            
        #     if re.match()
        # elif len(self.candidates) < len(self.error_chunk_lengths):
        #     print(len(self.candidates))
        # else:
        #     print(len(self.candidates))
        # # unaccounted = self.n_errors - self.n_certain_errors
        # # :if len(chunk) in self.certain_errors_chunks:

        # print()



def import_data(fn: str="12/input_test.txt") -> List[SpringLine]:
    with open(fn, 'r') as f:
        dat = f.readlines()
    dat = [line.split(" ")for line in dat]
    return [SpringLine.load(row[0], row[1]) for row in dat]

def main():
    dat = import_data()
    for x in dat:
        x.evaluate_options()
    print()


if __name__ == '__main__':
    main()