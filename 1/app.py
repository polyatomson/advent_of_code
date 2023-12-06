import re
from my_timer import my_timer

with open("1/input.txt", "r") as f:
        dat = f.readlines()

@my_timer
def part_one(dat):
    result = 0
    for line in dat:
        digits = re.findall("[0-9]", line)
        whole_digit = int("".join([digits[0], digits[-1]]))
        result += whole_digit
        
    print("result: ", result)

part_one(dat)

def normalize_digits(line):
    problematic = {"oneight": "oneeight",
        "twone": "twoone",
        "threeight": "threeeight",
        "fiveight": "fiveeight",
        "sevenine": "sevennine",
        "eightwo": "eighttwo",
        "eighthree": "eightthree",
        "nineight": "nineeight"}
    for k, v in problematic.items():
         line = line.replace(k, v)
    return line

@my_timer
def part_two(dat):
    digits_dic = {
          "one":"1", "two":"2", "three":"3", "four":"4", "five":"5", 
          "six":"6", "seven":"7", "eight":"8", "nine":"9",
          "1":"1", "2":"2", "3":"3", "4":"4", "5":"5", "6":"6", "7":"7", "8":"8", "9":"9"
          }
    regex = re.compile("one|two|three|four|five|six|seven|eight|nine|[0-9]")
    result = 0
    for line in dat:
        line = normalize_digits(line)
        digits = re.findall(regex, line)
        whole_digit = int("".join([digits_dic[digits[0]], digits_dic[digits[-1]]]))
        result += whole_digit
    print("result: ", result)


part_two(dat)