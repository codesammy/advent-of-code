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

def rules(n):
    rules = []
    rules.append(same_or_increasing_digits(n))
    rules.append(any(compare_adjacent_digits(n, same)))
    return all(rules)

def part1(text):
    lower, upper = tuple(map(int, text.split('-')))
    count = 0
    for i in range(lower, upper + 1):
        if rules(i):
            count += 1
    return count

assert_equals(rules(111111), True)
assert_equals(rules(223450), False)
assert_equals(rules(123789), False)

inputtext = "347312-805915"
print(part1(inputtext))
