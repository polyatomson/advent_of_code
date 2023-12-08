from dataclasses import dataclass
import re

@dataclass
class Race:
    time: int
    distance: int

    def button_options(self):
        max_button = self.time-1
        min_button = 1

        options = list()
        for button in range(min_button, max_button+1):
            time_left = self.time-button
            distance = button * time_left
            if distance > self.distance:
                options.append(button)
        return len(options)
    
def load_input(fn: str = "6/input.txt"):
    with open(fn, 'r') as f:
        dat = f.readlines()
    time_line = re.findall("[0-9]+", dat[0])
    distance_line = re.findall("[0-9]+", dat[1])
    races = [Race(time=int(n), distance=int(distance_line[i])) for i, n in enumerate(time_line)]
    return races

def load_input_part_two(fn: str = "6/input.txt"):
    with open(fn, 'r') as f:
        dat = f.read()
    dat = dat.replace(" ", "").split("\n")
    time_line = re.findall("[0-9]+", dat[0])
    distance_line = re.findall("[0-9]+", dat[1])
    race = Race(time=int(time_line[0]), distance=int(distance_line[0]))
    return race

def main():
    races = load_input()
    final_margin = 1
    for race in races:
        final_margin = final_margin * race.button_options()
    
    print("Part One result:", final_margin)
    
    race2 = load_input_part_two()
    final_margin2 = race2.button_options()
    print("Part Two result:", final_margin2)

if __name__ == "__main__":
    main()