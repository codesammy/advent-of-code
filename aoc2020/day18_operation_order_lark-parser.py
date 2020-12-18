import sys
sys.path.append('../')
from util import read_file, assert_equals

from lark import Lark, Transformer
import math

class PlusMulExprTransformer(Transformer):
    def expr(self, items):
        return items[0]
    def parenthesized(self, items):
        return items[0]
    def sum(self, items):
        return sum(items)
    def product(self, items):
        return math.prod(items)
    def NUMBER(self, items):
        return int(items)

# pip3 install lark-parser
# https://github.com/lark-parser/lark/blob/master/lark/grammars/common.lark
plus_mul_left_to_right = Lark('''
        ?expr: parenthesized
             | sop
      ?number: NUMBER
         ?sum: (sop "+")? number | (sop "+")? parenthesized
     ?product: (sop "*")? number | (sop "*")? parenthesized
         ?sop: sum | product
?parenthesized: "(" expr ")"
%import common.NUMBER
%import common.WS
%ignore WS
''', start="expr")

plus_before_mul = Lark('''
        ?expr: parenthesized
             | sop
      ?number: NUMBER
         ?sum: (sop "+")? number | (sop "+")? parenthesized
     ?product: (sop "*")? expr
         ?sop: product | sum
?parenthesized: "(" expr ")"
%import common.NUMBER
%import common.WS
%ignore WS
''', start="expr")

def part1(lines):
    def evaluate(line):
        parse_tree = plus_mul_left_to_right.parse(line)
        res = PlusMulExprTransformer().transform(parse_tree)
        return res
    return sum((evaluate(line) for line in lines))

def part2(lines):
    def evaluate(line):
        parse_tree = plus_before_mul.parse(line)
        res = PlusMulExprTransformer().transform(parse_tree)
        return res
    return sum((evaluate(line) for line in lines))

assert_equals(part1(["2 + 3 * 4"]), 20)
assert_equals(part1(["2 * 3 + (4 * 5)"]), 26)
assert_equals(part1(["5 + (8 * 3 + 9 + 3 * 4 * 3)"]), 437)
assert_equals(part1(["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"]), 12240)
assert_equals(part1(["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"]), 13632)

assert_equals(part2(["1 + (2 * 3) + (4 * (5 + 6))"]), 51)
assert_equals(part2(["2 * 3 + (4 * 5)"]), 46)
assert_equals(part2(["5 + (8 * 3 + 9 + 3 * 4 * 3)"]), 1445)
assert_equals(part2(["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"]), 669060)
assert_equals(part2(["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"]), 23340)

lines = read_file("day18_operation_order.input")
print(part1(lines))
print(part2(lines))
