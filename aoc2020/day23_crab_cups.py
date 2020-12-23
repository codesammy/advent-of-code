import sys
sys.path.append('../')
from util import read_file_one_string, assert_equals

from dataclasses import dataclass, field
from typing import Dict, List
from itertools import cycle, islice
import math

@dataclass
class Cup:
    label: str
    value: int
    next_cup: type = field(init=False)

    def __str__(self):
        return self.label

    def __lt__(self, other):
        return self.value < other.value

@dataclass
class Game:
    cups: List[Cup]
    max_value: int
    current_cup: Cup = field(init=False)
    one: Cup = field(init=False)
    lookup_by_value: Dict[int, Cup] = field(init=False, default_factory=dict)
    debug: bool = field(init=False, default=False)

    def __post_init__(self):
        self.current_cup = self.cups[0]
        self.one_cup = next(c for c in self.cups[:9] if c.value == 1)
        # link cups in circle
        last_cup = self.cups[-1]
        for cup in self.cups:
            last_cup.next_cup = cup
            last_cup = cup
            self.lookup_by_value[cup.value] = cup

    def move(self):
        a, b, c, first_picked_up_cup, last_picked_up_cup = self.pick_up()
        destination_cup = self.select_destination(a, b, c)
        self.place_cups(destination_cup, first_picked_up_cup, last_picked_up_cup)
        if self.debug:
            print(f"cups: {self}")
            print(f"pick up: {str(a)}, {str(b)}, {str(c)}")
            print(f"destination: {destination_cup.label}")
        self.select_new_current_cup()

    def pick_up(self):
        cup = self.current_cup
        a = self.current_cup.next_cup
        b = a.next_cup
        c = b.next_cup
        self.current_cup.next_cup = c.next_cup
        return a.value, b.value, c.value, a, c

    def select_destination(self, a, b, c):
        destination = None
        destination_value = self.current_cup.value - 1
        while destination == None:
            if destination_value == 0:
                destination_value = self.max_value
            if destination_value != a and destination_value != b and destination_value != c:
                destination = destination_value
                break
            destination_value -= 1
        return self.lookup_by_value[destination]

    def place_cups(self, destination_cup, first_picked_up_cup, last_picked_up_cup):
        temp = destination_cup.next_cup
        destination_cup.next_cup = first_picked_up_cup
        last_picked_up_cup.next_cup = temp

    def select_new_current_cup(self):
        self.current_cup = self.current_cup.next_cup

    def order(self):
        cup = self.one_cup
        order_cups = []
        for _ in range(len(self.cups) - 1):
            cup = cup.next_cup
            order_cups.append(cup)
        return "".join(map(str, order_cups))

    def product(self):
        a = self.one_cup.next_cup
        b = a.next_cup
        return a.value * b.value

    def __str__(self):
        return self.__str__cups(self.cups)

    def __str__cups(self, cups):
        def parens_around_current_cup(cup):
            if cup == self.current_cup:
                return '(' + str(cup) + ')'
            else:
                return str(cup)
        starting_cup = cups[0]
        cup = starting_cup
        str_cups = [cup]
        for _ in range(len(cups) - 1):
            cup = cup.next_cup
            str_cups.append(cup)
        return " ".join(map(parens_around_current_cup, str_cups))

def parse_input(text):
    for char in text:
        yield Cup(char, int(char))

def part1(text):
    cups = list(parse_input(text))
    game = Game(cups, 9)
    for _ in range(100):
        game.move()
    return game.order()

def part2(text):
    cups = list(parse_input(text))
    cups += list(map(lambda n: Cup(str(n), n), range(10, 1000000+1)))
    game = Game(cups, 1000000)
    for _ in range(10000000):
        game.move()
    return game.product()

sample = "389125467"
assert_equals(part1(sample), "67384529")
assert_equals(part2(sample), 149245887792)

inputtext = "364297581"
print(part1(inputtext))
print(part2(inputtext))
