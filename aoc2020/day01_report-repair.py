import sys
sys.path.append('../')

from util import read_file, assert_equals
from itertools import permutations
import math

def common(nums, num_operands=2):
    for operands in permutations(nums, num_operands):
        if sum(operands) == 2020:
            return math.prod(operands)

def part1(nums):
    return common(nums, 2)

def part2(nums):
    return common(nums, 3)

sample_array = [1721,979,366,299,675,1456]
assert_equals(part1(sample_array), 514579)
assert_equals(part2(sample_array), 241861950)

lines = read_file("day01_report-repair.input")
numbers = list(map(int, lines))

print(part1(numbers))
print(part2(numbers))
