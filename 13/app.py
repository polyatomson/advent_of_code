from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class Lava:
    rows: List[str]
    columns: List[str]
    n_rows: int
    n_col: int
    
    @staticmethod
    def import_lava(dat: List[str]) -> 'Lava':
        rows = dat
        cols = [''.join([row[y] for row in rows]) for y in range(len(rows[0]))]
        
        return Lava(rows, cols, len(rows), len(cols))
    
    def mirroring_vert(self, cut: int) -> Union[range, bool]:
        # max_steps = min(self.n_col-cut, cut)
        mirror_range = 0
        index_left = cut-1
        index_right = cut
        while index_left != -1 and index_right != self.n_col:
            if self.columns[index_left] == self.columns[index_right]:
                mirror_range = range(index_left, index_right+1)
                index_left -= 1
                index_right += 1
            else:
                break
        if mirror_range != 0:
            return mirror_range
        else:
            return False
    
    def mirroring_hor(self, cut: int) -> Union[range, bool]:
        # max_steps = min(self.n_rows-cut, cut)
        mirror_range = 0
        index_left = cut-1
        index_right = cut
        while index_left != -1 and index_right != self.n_rows:
            if index_left < 0:
                break
            if self.rows[index_left] == self.rows[index_right]:
                mirror_range = range(index_left, index_right+1)
                index_left -= 1
                index_right += 1
            else:
                break
        if mirror_range != 0:
            return mirror_range
        else:
            return False
        
    def find_mirror_vert(self) -> tuple:
        cuts = {}
        for cut in range(1, self.n_col):
            mirror = self.mirroring_vert(cut)
            if mirror:
                if mirror.start == 0 or mirror.stop == self.n_col:
                    cuts[cut] = len(mirror)
                    # if mirror.start == 0 and mirror.stop == self.n_rows:
                    #     print("ideal")
        if cuts == {}:
            return (0,0)
        else:
            # if len(cuts) > 1:
            #     print("ups")
            cuts = sorted(cuts.items(), key=lambda item: item[1])
            return cuts[-1]
    
    def find_mirror_hor(self) -> tuple:
        cuts = {}
        for cut in range(1, self.n_rows):
            mirror = self.mirroring_hor(cut)
            if mirror:
                if mirror.start == 0 or mirror.stop == self.n_rows:
                    cuts[cut] = len(mirror)
                    # if mirror.start == 0 and mirror.stop == self.n_rows:
                    #     print("ideal")
            else:
                continue
        if cuts == {}:
            return (0,0)
        else:
            # if len(cuts) > 1:
                # print("ups")
            cuts = sorted(cuts.items(), key=lambda item: item[1])
            return cuts[-1]

@dataclass
class Lavas:
    lavas: List[Lava]

    @staticmethod
    def import_dat(fn: str="13/input_test.txt") -> 'Lavas':
        with open(fn) as f:
            dat = f.read()
        lavas = [lava.split('\n') for lava in dat.split('\n\n')]
        return Lavas([Lava.import_lava(lava) for lava in lavas])
    
    def get_mirrors(self) -> int:
        result_vert = 0
        result_hor = 0

        for i, lava in enumerate(self.lavas):
            print(i)
            vert = lava.find_mirror_vert()
            hor = lava.find_mirror_hor()
            # if vert[1] == 0 and hor[1] == 0:
            #     print("ups")
            if vert[1] != 0:
                result_vert += vert[0]
                print(result_vert)
            elif hor[1] != 0:
                result_hor += hor[0]
        
        return result_vert + result_hor*100


def main():
    lavas = Lavas.import_dat("13/input.txt")
    res = lavas.get_mirrors()
    print("Part One result:", res)
    

if __name__ == "__main__":
    main()

