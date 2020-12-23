import sys
sys.path.append('../')
from util import read_file_one_string, assert_equals

from dataclasses import dataclass, field
from typing import List
from itertools import cycle, islice

@dataclass
class Cup:
    label: str

    def value(self):
        return int(self.label)

    def __str__(self):
        return self.label

    def __lt__(self, other):
        return self.label < other.label

@dataclass
class Game:
    cups: List[Cup]
    current_cup: Cup = field(init=False)
    move_count: int = field(default=1)

    def __post_init__(self):
        self.current_cup = self.cups[0]

    def move(self):
        print(f"-- move {self.move_count} --")
        print(f"cups: {self}")
        picked_up_cups = self.pick_up()
        print(f"pick up: {self.__str__cups(picked_up_cups)}")
        destination_cup = self.select_destination()
        print(f"destination: {destination_cup.label}")
        self.place_cups(destination_cup, picked_up_cups)
        self.select_new_current_cup()
        self.move_count += 1

    def pick_up(self, amount=3):
        current_cup_index = self.cups.index(self.current_cup)
        lookup_cups = self.cups*3
        picked_up_cups = lookup_cups[current_cup_index + 1:current_cup_index + 1 + amount]
        for picked in picked_up_cups:
            self.cups.remove(picked)
        return picked_up_cups

    def select_destination(self):
        lookup_cups = iter(cycle(reversed(sorted(self.cups))))
        while next(lookup_cups) != self.current_cup:
            pass
        return next(lookup_cups)

    def place_cups(self, destination_cup, picked_up_cups):
        destination_cup_index = self.cups.index(destination_cup)
        self.cups = self.cups[:destination_cup_index+1] + picked_up_cups + self.cups[destination_cup_index+1:]

    def select_new_current_cup(self):
        current_cup_index = self.cups.index(self.current_cup)
        lookup_cups = self.cups*2
        self.current_cup = lookup_cups[current_cup_index + 1]

    def order(self):
        cups = iter(cycle(self.cups))
        while next(cups).value() != 1:
            pass
        cups_after_one = islice(cups, 9-1)
        return "".join(map(str, cups_after_one))

    def __str__(self):
        return self.__str__cups(self.cups)

    def __str__cups(self, cups):
        def parens_around_current_cup(cup):
            if cup == self.current_cup:
                return '(' + str(cup) + ')'
            else:
                return str(cup)
        return " ".join(map(parens_around_current_cup, cups))

def parse_input(text):
    for char in text:
        yield Cup(char)

def part1(text):
    cups = list(parse_input(text))
    game = Game(cups)
    for _ in range(100):
        game.move()
    return game.order()

sample = "389125467"
assert_equals(part1(sample), "67384529")

inputtext = "364297581"
print(part1(inputtext))
