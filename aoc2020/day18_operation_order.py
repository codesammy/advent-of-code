import sys
import re
import math
sys.path.append('../')
from util import read_file, assert_equals

class MyNum:
    def __init__(self, num):
        self.num = num
    def __add__(self, other):
        return MyNum(self.num + other.num)
    def __mul__(self, other):
        return MyNum(self.num * other.num)
    def __sub__(self, other):
        return self * other
    def __and__(self, other):
        return self * other
    def __str__(self):
        return f"MyNum({self.num})"

def parse_input(line):
    num = re.compile(r"\d+")
    return line.replace("(", "( ").replace(")", " )").split(" ")

def calc(lines, ops):
    def repl(token):
        if str.isnumeric(token):
            return MyNum(int(token))
        elif token in '+*':
            return token.translate(str.maketrans('+*', ops))
        return token
    s = 0
    for line in lines:
        tokens = map(repl, parse_input(line))
        expr = "".join(map(str, tokens))
        res = eval(expr).num
        s += res
    return s

def part1(lines):
    return calc(lines, '+-')

def part2(lines):
    return calc(lines, '+&')

assert_equals(part1(["2 * 3"]), 6)
assert_equals(part1(["2 * 3 + (4 * 5)"]), 26)
assert_equals(part1(["5 + (8 * 3 + 9 + 3 * 4 * 3)"]), 437)
assert_equals(part1(["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"]), 12240)
assert_equals(part1(["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"]), 13632)

assert_equals(part2(["1 + (2 * 3) + (4 * (5 + 6))"]), 51)
assert_equals(part2(["2 * 3 + (4 * 5)"]), 46)
assert_equals(part2(["5 + (8 * 3 + 9 + 3 * 4 * 3)"]), 1445)
assert_equals(part2(["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"]), 669060)
assert_equals(part2(["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"]), 23340)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines))
print(part2(lines))
