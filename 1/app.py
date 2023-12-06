import re
from timer import my_timer

@my_timer
def part_one():
    with open("1/input.txt", "r") as f:
        dat = f.readlines()

    result = 0
    for line in dat:
        digits = re.findall("[0-9]", line)
        whole_digit = int("".join([digits[0], digits[-1]]))
        result += whole_digit
        
    print(result)

part_one()