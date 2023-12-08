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

def main():
    races = load_input()
    final_margin = 1
    for race in races:
        final_margin = final_margin * race.button_options()
    print(final_margin)

if __name__ == "__main__":
    main()