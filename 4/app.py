from dataclasses import dataclass
from typing import List
import re

@dataclass
class Card:
    id: int
    winning: List[int]
    given: List[int]

    @staticmethod
    def import_card(line: str):
        line = line.strip("\n")
        line = re.sub(" +", " ", line)
        id, numbers = line.split(": ")
        id = int(id.split(" ")[1])
        
        winning, given = numbers.split(" | ")

        winning = [int(n) for n in winning.split(" ")]
        given = [int(n) for n in given.split(" ")]
        
        return Card(id, winning, given)

    def won(self) -> int:
        won_ = [1 for n in self.given if n in self.winning]
        return sum(won_)
    
    def points(self) -> int:
        nwon = self.won()
        if nwon > 0:
            return 2**(nwon-1)
        else:
            return 0

        
def part_one(dat: List[str]) -> None:
    result = 0
    for line in dat:
        card = Card.import_card(line)
        card_points = card.points()
        result += card_points
    print(result)


def part_two(dat: List[str]) -> None:
    card_pile = [Card.import_card(line) for line in dat]
    results_pile = {card.id:[card.won()] for card in card_pile}
    #getcopies
    for id, ncopies_forward in results_pile.items():
        for ncopies in ncopies_forward:
            copies_range = range(id+1, id+1+ncopies)
            copies_ids = list(copies_range)
            for copy_id in copies_ids:
                results_pile[copy_id].append(results_pile[copy_id][0])
    flattened_results_pile = [card for ncopies in results_pile.values() 
                              for card in ncopies]
    print(len(flattened_results_pile))


def main(fn: str = "4/input.txt") -> None:
    with open(fn, 'r') as f:
        dat = f.readlines()
    part_one(dat)
    part_two(dat)

if __name__ == '__main__':
    main("4/input.txt")