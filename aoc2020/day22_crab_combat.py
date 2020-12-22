import sys
sys.path.append('../')
from util import read_file_one_string, assert_equals

from dataclasses import dataclass, field
from typing import List
from functools import reduce

@dataclass
class Player:
    name: str
    cards: List[int]

    def score(self):
        return reduce(lambda v,e: v+(e[0]+1)*e[1], enumerate(reversed(self.cards)), 0)

    def has_cards(self):
        return len(self.cards) > 0

@dataclass
class Game:
    players: List[Player]
    number: int = field(default=1)
    verbose: bool = field(default=False)
    recursive: bool = field(default=False)

    def play(self):
        self.memory = set()
        if self.verbose:
            print(f"=== Game {self.number} ===", end="\n\n")
        round_num = 0
        while all((p.has_cards() for p in self.players)):
            round_num += 1
            if self.verbose:
                print(f"-- Round {round_num} (Game {self.number}) --")
                print(f"Player 1's deck: {', '.join((str(c) for c in self.players[0].cards))}")
                print(f"Player 2's deck: {', '.join((str(c) for c in self.players[1].cards))}")

            current_hands = (self.players[0].score(), self.players[1].score())
            forever_condition = current_hands in self.memory
            self.memory.add(current_hands)

            if forever_condition:
                # due to the loop forever rule, the current game is won by Player 1
                self.winning_player = self.players[0]
                return
            else:
                if self.verbose:
                    print(f"Player 1 plays: {self.players[0].cards[0]}")
                    print(f"Player 2 plays: {self.players[1].cards[0]}")

                recursive_condition = all(len(p.cards[1:]) >= p.cards[0] for p in self.players)

                if recursive_condition and self.recursive:
                    # take only n cards into the subgame, excluding the top card with value n
                    subgame = Game([Player(p.name, p.cards[1:1+p.cards[0]]) for p in self.players], self.number + 1)
                    subgame.play()
                    winner = subgame.winning_player.name
                    if self.verbose:
                        print(f"...anyway, back to game {self.number}.")
                else:
                    if self.players[0].cards[0] > self.players[1].cards[0]:
                        winner = 'Player 1'
                    else:
                        winner = 'Player 2'
            if self.verbose:
                print(f"{winner} wins round_num {round_num} of game {self.number}!", end="\n\n")
            if winner == 'Player 1':
                self.players[0].cards = self.players[0].cards[1:] + [self.players[0].cards[0], self.players[1].cards[0]]
                self.players[1].cards = self.players[1].cards[1:]
            else:
                self.players[1].cards = self.players[1].cards[1:] + [self.players[1].cards[0], self.players[0].cards[0]]
                self.players[0].cards = self.players[0].cards[1:]
        self.winning_player = next((p for p in self.players if p.has_cards()))
        if self.verbose:
            print(f"The winner of game {self.number} is {self.winning_player.name}!")

def parse_input(text):
    for block in text.split('\n\n'):
        yield Player(block.strip().split('\n')[0][:-1], [int(x) for x in block.strip().split('\n')[1:]])

def part1(text):
    players = list(parse_input(text))
    game = Game(players, recursive=False)
    game.play()
    return game.winning_player.score()

def part2(text):
    players = list(parse_input(text))
    game = Game(players, recursive=True)
    game.play()
    return game.winning_player.score()

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
assert_equals(part2(sample1), 291)

sample2 = """Player 1:
43
19

Player 2:
2
29
14"""
part2(sample2)

inputtext = read_file_one_string(sys.argv[0].replace("py", "input"))
print(part1(inputtext))
print(part2(inputtext))
