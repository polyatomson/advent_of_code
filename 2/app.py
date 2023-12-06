
import re
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Round:
    blue: int
    green: int
    red: int

    def import_balls(balls: dict):
        if 'blue' in balls:
            blue = balls['blue']
        else:
            blue = 0
        if 'green' in balls:
            green = balls['green']
        else:
            green = 0
        if 'red' in balls:
            red = balls['red']
        else:
            red = 0
        
        return Round(blue, green, red)
    

@dataclass
class Game:
    id: int
    rounds: List[Round]

    def checkifgameispossible(self, given_blue: int, given_green: int, given_red: int) -> int:
        maxblue = max([r.blue for r in self.rounds])
        maxgreen = max([r.green for r in self.rounds])
        maxred = max([r.red for r in self.rounds])
        if given_blue >= maxblue and given_green >= maxgreen and given_red >= maxred:
            return self.id
        else:
            return 0



def parsegames(line):
    id, game = line.split(': ')
    id = int(re.findall("[0-9]+", id)[0])
    rounds = game.split("; ")
    game = Game(id, [])
    for r in rounds:
        balls = re.findall("([0-9]+) ([a-z]+)?(?:,|$)", r)
        balls = {col[1]:int(col[0]) for col in balls}
        r = Round.import_balls(balls)
        game.rounds.append(r)
    return game


def cheking_all_games(dat):
    id_sum = 0
    for line in dat:
        game = parsegames(line)
        game_result = game.checkifgameispossible(given_blue=14, given_green=13, given_red=12)
        id_sum += game_result
    return id_sum

def main():
    with open("2/input.txt", "r") as f:
        dat = f.readlines()
    result = cheking_all_games(dat)
    print("result:", result)

if __name__ == '__main__':
    main()