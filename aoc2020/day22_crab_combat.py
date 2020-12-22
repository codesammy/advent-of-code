import sys
sys.path.append('../')
from util import read_file_one_string, assert_equals

from dataclasses import dataclass, field
from typing import List
from functools import reduce

@dataclass
class Player:
    cards: List[int]

    def fight(self, other):
        my_card = self.cards[0]
        other_card = other.cards[0]
        if my_card > other_card:
            self.cards = self.cards[1:] + [my_card, other_card]
            other.cards = other.cards[1:]
        else:
            other.cards = other.cards[1:] + [other_card, my_card]
            self.cards = self.cards[1:]

    def score(self):
        return reduce(lambda v,e: v+(e[0]+1)*e[1], enumerate(reversed(self.cards)), 0)

    def has_cards(self):
        return len(self.cards) > 0

def parse_input(text):
    for block in text.split('\n\n'):
        yield Player([int(x) for x in block.strip().split('\n')[1:]])

def part1(text):
    players = list(parse_input(text))
    while all((p.has_cards() for p in players)):
        players[0].fight(players[1])
    winning_player = next((p for p in players if p.has_cards()))
    return winning_player.score()

sample1 = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""
assert_equals(part1(sample1), 306)

inputtext = read_file_one_string(sys.argv[0].replace("py", "input"))
print(part1(inputtext))
