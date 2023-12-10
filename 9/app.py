from dataclasses import dataclass
from typing import List

@dataclass
class History:
    history: List[List[int]]

    def __str__(self):
        pretty_lines = list()
        for i, line in enumerate(self.history):
            indent = "  "*(i+1)
            pretty_line = indent + "   ".join([str(n) for n in line])
            pretty_lines.append(pretty_line)
        
        pretty_lines = "\n".join(pretty_lines)
        
        return pretty_lines

    @staticmethod
    def create_differences(line: List[int]) -> List[int]:
        differences = [line[i] - line[i-1] for i in range(1, len(line))]
        return differences
    

    @staticmethod
    def import_history(line: List[str]):
        line = [int(n) for n in line]
        history = [line]
        while all([n == 0 for n in line]) is not True:
            line = History.create_differences(line)
            history.append(line)
        return History(history)
    
    def predict(self) -> None:
        self.history[-1].append(0)
        history_reversed = list(reversed(self.history))
        for i, line in enumerate(history_reversed[:-1]):
            prediction = line[-1] + history_reversed[i+1][-1]
            history_reversed[i+1].append(prediction)
    
    def get_predictions(self) -> List[int]:
        return self.history[0][-1]



def import_data(fn: str="9/input.txt") -> List[History]:
    with open(fn, 'r') as f:
        dat = f.readlines()
    lines = [line.strip("\n").split(" ") for line in dat]
    histories = [History.import_history(line) for line in lines]
    return histories

def main():
    histories = import_data()
    all_predicted = 0
    for history in histories:
        history.predict()
        predicted = history.get_predictions()
        all_predicted += predicted
    print("Part 1 result:", all_predicted)

if __name__ == "__main__":
    main()


    