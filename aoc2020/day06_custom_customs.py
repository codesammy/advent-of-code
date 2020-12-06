import sys
from functools import reduce
sys.path.append('../')
from util import read_file, assert_equals

class Person:
    def __init__(self, line):
        self.answers = set((x for x in line))

class Group:
    def __init__(self):
        self.persons = []
        
    def add(self, person):
        self.persons.append(person)

    def anyone_yes(self):
        return reduce(set.union, (p.answers for p in self.persons))

    def everyone_yes(self):
        return reduce(set.intersection, (p.answers for p in self.persons))
    
def parse_groups(lines):
    groups = []
    g = Group()
    groups.append(g)
    for line in lines:
        if line == "":
            g = Group()
            groups.append(g)
        else:
            g.add(Person(line))
    return groups

def part1(lines):
    groups = parse_groups(lines)
    return sum(map(len, map(Group.anyone_yes, groups)))

def part2(lines):
    groups = parse_groups(lines)
    return sum(map(len, map(Group.everyone_yes, groups)))

sample = """abc

a
b
c

ab
ac

a
a
a
a

b""".split("\n")
assert_equals(part1(sample), 11)
assert_equals(part2(sample), 6)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines))
print(part2(lines))
