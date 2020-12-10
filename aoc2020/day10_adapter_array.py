import sys
sys.path.append('../')
from util import read_file, assert_equals
from collections import defaultdict
from functools import reduce
import math

def acceptable_joltages(joltage):
    return [joltage - i for i in range(1,4)]

def part1(nums):
    adapters = nums.copy()
    my_adapter_joltage = max(nums) + 3
    final_path = []
    def find_longest_path(start, path):
        for j in acceptable_joltages(start):
            if j in adapters and j not in path:
                if 0 in acceptable_joltages(j) and len(adapters) - len(path) == 1:
                    return path + [j]
                newpath = path.copy()
                newpath.append(j)
                rv = find_longest_path(j, newpath)
                if rv:
                    return rv
        return False

    final_path = find_longest_path(my_adapter_joltage, []) + [0];
    diffs = defaultdict(lambda: 0)
    i = my_adapter_joltage
    for j in final_path:
        diff = i-j
        diffs[diff] += 1
        i = j
    return math.prod(diffs.values())

def part2(nums):
    def count_distinct_paths_for_subgraph(adapters):
        return count_distinct_paths(max(adapters)+3, max(min(adapters)-3,0), [], adapters)

    def count_distinct_paths(start, end, path, adapters):
        distinct_paths = 0
        i = 1
        for adapter in set(acceptable_joltages(start)) & set(adapters) - set(path):
            i+=1
            if end in acceptable_joltages(adapter):
                distinct_paths += 1
            newpath = path.copy()
            newpath.append(adapter)
            distinct_paths += count_distinct_paths(adapter, end, newpath, adapters)
        return distinct_paths

    # sort all nums
    nums = sorted(nums)

    # split graphs into subgraphs when adapters are 3 joltages apart
    subgraphs = reduce(lambda v,i: v + [[nums[i]]] if nums[i]-(v[-1][-1] if len(v[-1]) > 0 else 0)==3 else v[:-1] + [v[-1]+[nums[i]]], range(len(nums)), [[]])

    # multiply counts of distinct paths in subgraphs to get the total count of distinct paths
    return math.prod(map(count_distinct_paths_for_subgraph, subgraphs))

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
assert_equals(part2(sample1), 8)

sample2 = list(map(int,"""28
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
assert_equals(part1(sample2), 220)
assert_equals(part2(sample2), 19208)

nums = list(map(int,read_file(sys.argv[0].replace("py", "input"))))
print(part1(nums))
print(part2(nums))

