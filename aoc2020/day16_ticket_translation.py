import sys
from itertools import takewhile, product
from collections import defaultdict
import re
import math
sys.path.append('../')
from util import read_file, assert_equals

class Field:
    field_pattern = re.compile(r"([^:]+): (\d+)-(\d+) or (\d+)-(\d+)")

    def __init__(self, name, min1, max1, min2, max2):
        self.name = name
        self.min1 = min1
        self.max1 = max1
        self.min2 = min2
        self.max2 = max2

    def contains(self, value):
        return (self.min1 <= value <= self.max1) or (self.min2 <= value <= self.max2)

    def __repr__(self):
        return f"Field({repr(self.name)},{repr(self.min1)},{repr(self.max1)},{repr(self.min2)},{repr(self.max2)})"

    def __hash__(self):
        return hash(self.name)

    @classmethod
    def of(cls, line):
        name, min1, max1, min2, max2 = Field.field_pattern.fullmatch(line).groups()
        return Field(name, int(min1), int(max1), int(min2), int(max2))

class Ticket:
    def __init__(self, nums):
        self.nums = nums

    def validate(self, fields):
        return [v for v in self.nums if all((not f.contains(v) for f in fields))]

    def is_valid(self, fields):
        return len(self.validate(fields)) == 0

    def assign_fields(self, fields_sorted):
        for i,f in enumerate(fields_sorted):
            f.value = self.nums[i]
        self.fields = fields_sorted

    def __repr__(self):
        return f"Ticket({repr(self.nums)})"

    @classmethod
    def of(cls, line):
        return Ticket([int(n) for n in line.split(",")])

def parse_input(lines):
    it = iter(lines)
    field_lines = takewhile(lambda x: x != "", it)
    fields = [Field.of(line) for line in field_lines]
    next(it)
    my_ticket = Ticket.of(next(it))
    next(it);next(it)
    nearby_tickets = [Ticket.of(x) for x in it]

    return fields, my_ticket, nearby_tickets

def part1(lines):
    fields, my_ticket, nearby_tickets = parse_input(lines)
    return sum(value for ticket in nearby_tickets for value in ticket.validate(fields))

def part2(lines):
    def compute_fields_sorted(fields, my_ticket, nearby_tickets):
        valid_tickets = [t for t in nearby_tickets if t.is_valid(fields)]

        possible = defaultdict(set)
        found = defaultdict(int)
        for pos in range(len(fields)):
            for f in fields:
                possible[f].add(pos)
                for t in valid_tickets:
                    if not f.contains(t.nums[pos]):
                        possible[f].remove(pos)

        while len(possible) > 0:
            found_field = next(f for f in possible if len(possible[f]) == 1)
            found_pos = possible[found_field].pop()
            found[found_pos] = found_field
            for f in possible.copy():
                if found_pos in possible[f]:
                    possible[f].remove(found_pos)
            del possible[found_field]

        fields_sorted = list(map(lambda i: found[i], range(len(fields))))
        return fields_sorted

    fields, my_ticket, nearby_tickets = parse_input(lines)
    fields_sorted = compute_fields_sorted(fields, my_ticket, nearby_tickets)
    my_ticket.assign_fields(fields_sorted)
    return math.prod([f.value for f in my_ticket.fields if f.name.startswith("departure")])

sample1 = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12""".split("\n")
assert_equals(part1(sample1), 71)

sample2 = """departure a: 0-1 or 4-19
departure b: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9""".split("\n")
assert_equals(part2(sample2), 132)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines))
print(part2(lines))
