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
    move_count: int = field(default=1)
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
        picked_up_cups = self.pick_up()
        destination_cup = self.select_destination(picked_up_cups)
        self.place_cups(destination_cup, picked_up_cups)
        if self.debug:
            print(f"-- move {self.move_count} --")
            print(f"cups: {self}")
            print(f"pick up: {self.__str__cups(picked_up_cups)}")
            print(f"destination: {destination_cup.label}")
        self.select_new_current_cup()
        self.move_count += 1

    def pick_up(self, amount=3):
        picked_up_cups = [self.current_cup.next_cup]
        picked_up_cups += [picked_up_cups[-1].next_cup]
        picked_up_cups += [picked_up_cups[-1].next_cup]

        self.current_cup.next_cup = picked_up_cups[-1].next_cup
        return picked_up_cups

    def select_destination(self, picked_up_cups):
        destination = None
        start_value = self.current_cup.value - 1
        picked_up_values = list(map(lambda c: c.value, picked_up_cups))
        local_max_value = max(set(range(self.max_value-3,self.max_value+1))-set(picked_up_values))
        while destination == None:
            if start_value == 0:
                start_value = local_max_value
            if start_value not in picked_up_values:
                destination = start_value
            start_value -= 1
        return self.lookup_by_value[destination]

    def place_cups(self, destination_cup, picked_up_cups):
        temp = destination_cup.next_cup
        destination_cup.next_cup = picked_up_cups[0]
        picked_up_cups[-1].next_cup = temp

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
