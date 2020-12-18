import sys
import re
import math
sys.path.append('../')
from util import read_file, assert_equals

class BiOp:
    def __init__(self):
        self.op = None
        self.operand1 = None
        self.operand2 = None

    def execute(self):
        if self.op == '+':
            return self.operand1 + self.operand2
        else:
            return self.operand1 * self.operand2

    def __repr__(self):
        return f"BiOp({repr(self.op)},{repr(self.operand1)},{repr(self.operand2)})"

def parse_input(line):
    num = re.compile(r"\d+")
    return line.replace("(", "( ").replace(")", " )").split(" ")

def eval_expr(line):
    tokens = parse_input(line)
    stack = [[]]
    p = 0
    value = 0
    last = None
    for i,token in enumerate(tokens):
        if str.isnumeric(token):
            if last and last in '+*':
                op = stack[p][-1]
                op.operand2 = int(token)
                op.operand1 = op.execute()
                op.operand2 = None
                op.op = None
            else:
                op = BiOp()
                op.operand1 = int(token)
                stack[p].append(op)
        elif token in '*+':
            op = stack[p][-1]
            op.op = token
        elif token in '(':
            p+=1
            stack.append([])
        elif token in ')':
            op = stack[p][-1]
            del stack[p]
            p-=1
            if len(stack[p]) > 0:
                prev_op = stack[p][-1]
                prev_op.operand2 = op.operand1
                prev_op.operand1 = prev_op.execute()
                prev_op.operand2 = None
                prev_op.op = None
            else:
                stack[p].append(op)
        last = token
    return stack[p][-1].operand1

def part1(lines):
    return sum((eval_expr(line) for line in lines))

class MyNum:
    def __init__(self, num):
        self.num = num
    def __mul__(self, other):
        return MyNum(self.num + other.num)
    def __add__(self, other):
        return MyNum(self.num * other.num)
    def __str__(self):
        return f"MyNum({self.num})"

def part2(lines):
    def repl(token):
        if str.isnumeric(token):
            return MyNum(int(token))
        if token in '+*':
            return token.translate(str.maketrans('+*', '*+'))
        return token
    s = 0
    for line in lines:
        tokens = map(repl, parse_input(line))
        expr = "".join(map(str, tokens))
        res = eval(expr).num
        s += res
    return s

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
