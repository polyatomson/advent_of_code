from typing import List

with open('14/input.txt', 'r') as f:
    dat = f.readlines()

dat = [list(line.strip('\n')) for line in dat]

def tilt(dat: List[List[str]]):
    changed = False
    for i, line in enumerate(dat[:-1]):
        for position, item in enumerate(line):
            if item == '.':
                if dat[i+1][position] == 'O':
                    line[position] = 'O'
                    dat[i+1][position] = '.'
                    changed = True
        # print(line)
        dat[i] = line
    return changed, dat

changed = True

while changed:
    changed, dat = tilt(dat)

res = 0
for i, line in enumerate(reversed(dat)):
    # print(''.join(line))
    ows = [1 for char in line if char == 'O']
    res += sum(ows) * (i+1)

print(res)