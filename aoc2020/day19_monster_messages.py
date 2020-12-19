import sys
sys.path.append('../')
from util import read_file, assert_equals

from itertools import takewhile
from lark import Lark, Transformer
import math
import re

def use_lark(lines, mod=lambda x: x):
    it = iter(lines)
    grammar = "\n".join(takewhile(lambda l: l != '', it))
    grammar = mod(grammar)
    grammar = re.sub(r'(\d+)', r'a\1', grammar)
    lines = list(it)
    lark = Lark(grammar, start="a0")
    def is_valid(line):
        res = False
        try:
            parse_tree = lark.parse(line)
            res = True
        except:
            pass
        return res
    return sum((1 for line in lines if is_valid(line)))

def part1(lines):
    def identity(x):
        return x
    return use_lark(lines, identity)

def part2(lines):
    def mod(grammar):
        grammar = re.sub(r'8: 42', r'8: 42 | 42 8', grammar)
        grammar = re.sub(r'11: 42 31', r'11: 42 31 | 42 11 31', grammar)
        return grammar
    return use_lark(lines, mod)

sample1 = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb""".split("\n")
assert_equals(part1(sample1), 2)

sample2 = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba""".split("\n")
assert_equals(part2(sample2), 12)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines))
print(part2(lines))
