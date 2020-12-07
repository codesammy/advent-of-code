import sys
import re
sys.path.append('../')
from util import read_file, assert_equals

class BagRuleParser:
    no_other_bags_pattern = re.compile("(.+) bags contain no other bags.")
    contains_bags_pattern = re.compile(r"(.+) bags contain (\d.+)")
    bag_pattern = re.compile(r"(\d+) ([^,.]+?) bags?")
    
    def __init__(self):
        self.rules = dict()

    def parse_line(self, line):
        if m := self.no_other_bags_pattern.fullmatch(line):
            color = m.group(1)
            if color not in self.rules:
                self.rules[color] = BagRule(color)
        elif m := self.contains_bags_pattern.fullmatch(line):
            color = m.group(1)
            if color not in self.rules:
                self.rules[color] = BagRule(color)
            for count, other_color in self.bag_pattern.findall(m.group(2)):
                if other_color not in self.rules:
                    self.rules[other_color] = BagRule(other_color)
                self.rules[color].children.add(self.rules[other_color])
                self.rules[other_color].parents.add(self.rules[color])
        else:
            raise Exception(f"unknown rule: {line}")

    def __repr__(self):
        return f"BagRuleParser(rules={self.rules})"

class BagRule:
    def __init__(self, color):
        self.color = color
        self.parents = set()
        self.children = set()

    def accept_up(self, visitor):
        for p in self.parents:
            visitor.visit(p)
            p.accept_up(visitor)

    def __repr__(self):
        return self.__str__()
        
    def __str__(self):
        return f'BagRule("{self.color}",parents={len(self.parents)},children={len(self.children)})'

class BagRuleParentVisitor:
    def __init__(self):
        self.colors = set()

    def visit(self, bag_rule):
        self.colors.add(bag_rule.color)
    
def part1(lines, my_bag_color):
    rules = BagRuleParser()
    for l in lines:
        rules.parse_line(l)
    parent_visitor = BagRuleParentVisitor()
    rules.rules[my_bag_color].accept_up(parent_visitor)
    return len(parent_visitor.colors)

sample = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.""".split("\n")
assert_equals(part1(sample, "shiny gold"), 4)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines, "shiny gold"))
