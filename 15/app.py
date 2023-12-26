from dataclasses import dataclass
from typing import List
import re

with open("15/input.txt", 'r') as f:
    dat = f.read()

dat.replace('\n', '')
dat = dat.split(',')

def hash(line: str):
    current = 0
    for char in line:
        current += ord(char)
        current *= 17
        current = current%256
    return current

records = {hash(record):record for record in dat}
print("Part one result:", sum(records))
records = {record:hash(re.split('-|=', record)[0]) for record in dat}



@dataclass
class Box:
    order: List[str]
    focal_lengths: dict[str, int]

boxes = {box_id:Box([], {}) for box_id in records.values()}

# print(boxes)
for record, box_id in records.items():
    if '=' in record:
        code, focal_length = record.split('=')
        if code not in boxes[box_id].order:
            boxes[box_id].order.append(code)
        boxes[box_id].focal_lengths[code] = focal_length
    elif '-' in record:
        code = record.strip('-')
        if code in boxes[box_id].order:
            place = boxes[box_id].order.index(code)
            boxes[box_id].order.pop(place)
            boxes[box_id].focal_lengths.pop(code)
    # print(box_id, boxes[box_id])

# lenses = {re.split('-|=', record)[0] for record in dat}

total = 0
for box_id, box in boxes.items():
    print(box_id, box.focal_lengths)
    for i, lens in enumerate(box.order):
        slot = i+1
        focal_length = box.focal_lengths[lens]
        box_n = box_id+1
        lens_val = slot * int(focal_length) * box_n
        total += lens_val
print(total)

# for 





