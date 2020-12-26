import sys
sys.path.append('../')
from util import read_file, assert_equals

from itertools import count
import math

def same(a, b):
    return a == b

def increasing(a, b):
    return a < b

def same_or_increasing(a, b):
    return same(a, b) or increasing(a, b)

def same_or_increasing_digits(n):
    return all(compare_adjacent_digits(n, same_or_increasing))

def compare_adjacent_digits(n, pred):
    it = iter(str(n))
    last = next(it)
    for digit in it:
        yield pred(int(last), int(digit))
        last = digit

def same_groups(n):
    it = iter(str(n))
    group = [next(it)]
    for digit in it:
        last = group[-1]
        if digit == last:
            group.append(digit)
        else:
            if len(group) > 1:
                yield group
            group = [digit]
    if len(group) > 1:
        yield group

def rules_part1(n):
    rules = []
    rules.append(same_or_increasing_digits(n))
    rules.append(any(compare_adjacent_digits(n, same)))
    return all(rules)

def rules_part2(n):
    rules = []
    rules.append(same_or_increasing_digits(n))
    rules.append(any(len(x) == 2 for x in same_groups(n)))
    return all(rules)

def parse_input(text):
    return tuple(map(int, text.split('-')))

def part1(text):
    lower, upper = parse_input(text)
    return sum(1 for i in range(lower, upper + 1) if rules_part1(i))

def part2(text):
    lower, upper = parse_input(text)
    return sum(1 for i in range(lower, upper + 1) if rules_part2(i))

assert_equals(rules_part1(111111), True)
assert_equals(rules_part1(223450), False)
assert_equals(rules_part1(123789), False)

assert_equals(rules_part2(112233), True)
assert_equals(rules_part2(123444), False)
assert_equals(rules_part2(111122), True)
assert_equals(rules_part2(112223), True)

inputtext = "347312-805915"
print(part1(inputtext))
print(part2(inputtext))
