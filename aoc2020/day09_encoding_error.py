import sys
from itertools import combinations
sys.path.append('../')
from util import read_file, assert_equals

def part1(lines, preamble):
    nums = [int(n) for n in lines]
    i = preamble
    buf = nums[:i]
    while True:
        n = nums[i]
        if n not in (a+b for a,b in combinations(buf, 2)):
            return n
        buf = buf[1:] + [n]
        i += 1

def part2(lines, preamble):
    weak = part1(lines, preamble)
    nums = [int(n) for n in lines]
    return next(min(c)+max(c) for a in range(len(nums)) for b in range(a+1,len(nums)) for c in [nums[a:b]] if sum(c) == weak)

sample = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576""".split("\n")
assert_equals(part1(sample, 5), 127)
assert_equals(part2(sample, 5), 62)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines, 25))
print(part2(lines, 25))
