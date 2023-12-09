from dataclasses import dataclass
from typing import List, Any, Tuple
from collections import Counter

@dataclass
class Hand:
    cards: List[int]
    type: int
    bid: int

    def convert_cards(cards: List[str]):
        card_values = {
            "A":14, "K":13, "Q":12, "J":11, "T":10, "9":9, "8":8, 
            "7":7, "6":6, "5":5, "4":4, "3":3, "2":2
            }
        return [card_values[card] for card in cards]
    
    def convert_cards_w_jokers(cards: List[str]):
        card_values = {
            "A":13, "K":12, "Q":11, "T":10, "9":9, "8":8, 
            "7":7, "6":6, "5":5, "4":4, "3":3, "2":2, "J":1
            }
        return [card_values[card] for card in cards]

    def define_type(cards: List[int]) -> int:
        card_counter = Counter(cards)

        if len(card_counter) == 1:
            return 7 # five of a kind
        elif len(card_counter) == 2:
            if max(card_counter.values()) == 4:
                return 6 #four of a kind
            else:
                return 5 #fullhouse
        elif len(card_counter) == 3:
            if max(card_counter.values()) == 3:
                return 4 #three of a kind
            else:
                return 3 #two pairs
        elif len(card_counter) == 4:
            return 2 #one pair
        elif len(card_counter) == 5:
            return 1 #high card
    
    def define_type_w_jokers(cards: List[int]) -> int:
        if 1 in cards:
            card_to_frequency = Counter(cards).most_common()
            frequency_to_card = [(record[1], record[0]) for record in card_to_frequency]
            optimal_card_to_replace = sorted(frequency_to_card)[-1][1]
            replace_w_joker = lambda joker, card: joker if card == 1 else card
            new_cards = [replace_w_joker(optimal_card_to_replace, card) for card in cards]
        else:
            new_cards = cards
        return Hand.define_type(new_cards)



    @staticmethod
    def import_hand(hand_raw: List[Any], w_jokers: bool):
        bid = hand_raw[1]
        if w_jokers:
            cards = Hand.convert_cards_w_jokers(hand_raw[0])
            type = Hand.define_type_w_jokers(cards)
        else:
            cards = Hand.convert_cards(hand_raw[0])
            type = Hand.define_type(cards)
        return Hand(cards=cards, type=type, bid=bid)
    
    def as_tuple(self) -> tuple:
        hand_as_tuple = [self.type]
        hand_as_tuple.extend(self.cards)
        hand_as_tuple.append(self.bid)
        return tuple(hand_as_tuple)
    
    @staticmethod
    def from_tuple(hand_as_tuple: Tuple[int]):
        return Hand(type=hand_as_tuple[0], cards=hand_as_tuple[1:6], bid=hand_as_tuple[6])

@dataclass
class Hands:
    hands: List[Hand]

    def order_hands(self):
        hands_as_tuples = [hand.as_tuple() for hand in self.hands]
        sorted_hands = sorted(hands_as_tuples)
        print(sorted_hands[-10:-1])
        return Hands([Hand.from_tuple(hand) for hand in sorted_hands])
    
    def count_points(self) -> int:
        hands_points = [hand.bid * (i+1) for i, hand in enumerate(self.hands)]
        return sum(hands_points)


def main(fn: str = "7/input_test.txt"):
    with open(fn, "r") as f:
        dat = f.readlines()
    lines_split = [line.split(" ") for line in dat]
    hands_raw = [[list(line[0]), int(line[1])] for line in lines_split]
    #Part One
    hands = Hands([Hand.import_hand(hand_raw, w_jokers=False) for hand_raw in hands_raw])
    hands_ordered = hands.order_hands()
    total_points = hands_ordered.count_points()
    print("Part One result:", total_points)
    
    #Part Two
    hands = Hands([Hand.import_hand(hand_raw, w_jokers=True) for hand_raw in hands_raw])
    hands_ordered = hands.order_hands()
    total_points = hands_ordered.count_points()
    print("Part Two result:", total_points)


if __name__ == "__main__":
    main()