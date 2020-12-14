import sys
from operator import itemgetter
import math
import re
sys.path.append('../')
from util import read_file, assert_equals

class BitMask:
    def __init__(self, mask):
        # force 1
        self.or_mask = int(mask.translate({ord("X"):"0"}), 2)
        # force 0
        self.and_mask = int(mask.translate({ord("X"):"1"}), 2)
    def apply(self, bits):
        res = (bits & self.and_mask) | self.or_mask
        return res

class MaskInstruction:
    def __init__(self, mask):
        self.mask = mask

    def execute(self, program):
        program.mask = BitMask(self.mask)

class MemoryInstruction:
    instruction_pattern = re.compile(r"mem\[(\d+)\] = (\d+)")
    def __init__(self, addr, num):
        self.addr = addr
        self.num = num

    def execute(self, program):
        program.memory[self.addr] = program.mask.apply(self.num)

class Program:
    def __init__(self):
        self.memory = {}
        self.mask = BitMask("X"*36)

    def run(self, instructions):
        for i in instructions:
            i.execute(self)

def parse_input(lines):
    instructions = []
    for line in lines:
        if line[:3] == "mas":
            mask = line[7:]
            yield MaskInstruction(mask)
        if line[:3] == "mem":
            addr, num = MemoryInstruction.instruction_pattern.fullmatch(line).groups()
            yield MemoryInstruction(int(addr), int(num))

def part1(instructions):
    p = Program()
    p.run(instructions)
    return sum(p.memory.values())

sample1 = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0""".split("\n")
assert_equals(part1(parse_input(sample1)), 165)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(parse_input(lines)))
