import sys
from operator import sub
from functools import reduce
from itertools import chain
from collections import defaultdict
from queue import SimpleQueue
import re
sys.path.append('../')
from util import read_file, assert_equals

class MemoryGameNumbers:

    def __init__(self, starting_numbers=[0]):
        self.starting_numbers = starting_numbers

    def __iter__(self):
        self.memory = defaultdict(list)
        self.spoken_count = defaultdict(int)
        self.turn = 0
        return self

    def __next__(self):
        self.turn += 1
        res = 0

        try:
            res = next(self.starting_numbers)
        except StopIteration:
            # first time -> 0
            if self.spoken_count[self.last_num] == 1:
                res = 0
            else:
                # otherwise turn difference
                res = abs(sub(*self.memory[self.last_num][-2:]))

        self.memory[res].append(self.turn)
        # save memory for part2
        if len(self.memory[res]) > 2:
            self.memory[res] = self.memory[res][-2:]
        self.last_num = res
        self.spoken_count[res] += 1
        return res

    def compute_next(self):
        return 1

def parse_input(line):
    for num in line.split(","):
        yield int(num)

def part1(line, nth_element):
    starting_numbers = parse_input(line)
    return next(x for i,x in enumerate(MemoryGameNumbers(starting_numbers)) if i==nth_element-1)

part2 = part1

sample1 = "0,3,6"
assert_equals(part1(sample1, 2020), 436)
assert_equals(part2(sample1, 30000000), 175594)

line = "14,1,17,0,3,20"
print(part1(line, 2020))
print(part2(line, 30000000))
