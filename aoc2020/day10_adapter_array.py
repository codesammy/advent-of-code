import sys
sys.path.append('../')
from util import read_file, assert_equals
from collections import defaultdict
import math

def part1(nums):
    def acceptable_joltages(joltage):
        return [joltage - i for i in range(1,4)]
    adapters = nums.copy()
    differences = dict()
    my_adapter_joltage = max(nums) + 3

    final_path = []
    def go(start, path):
        for j in acceptable_joltages(start):
            if j in adapters and j not in path:
                if 0 in acceptable_joltages(j) and len(adapters) - len(path) == 1:
                    return path + [j]
                newpath = path.copy()
                newpath.append(j)
                rv = go(j, newpath)
                if rv:
                    return rv
        return False

    final_path = go(my_adapter_joltage, []) + [0];
    diffs = defaultdict(lambda: 0)
    i = my_adapter_joltage
    for j in final_path:
        diff = i-j
        diffs[diff] += 1
        i = j
    return math.prod(diffs.values())

sample1 = list(map(int,"""16
10
15
5
1
11
7
19
6
12
4""".split("\n")))
assert_equals(part1(sample1), 35)

sample1 = list(map(int,"""28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3""".split("\n")))
assert_equals(part1(sample1), 220)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(list(map(int,lines))))

