import sys
from operator import or_
from functools import reduce
from itertools import combinations_with_replacement
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

class FloatingBitMask:
    def __init__(self, mask):
        # force 1
        self.or_mask = int(mask.translate({ord("X"):"0"}), 2)
        # force 0
        self.and_mask = int(mask.translate({ord("X"):"0", ord("0"):"1"}), 2)
        self.floating_nums = {reduce(or_, x) for x in combinations_with_replacement([2**i for i, b in enumerate(reversed(mask)) if b == 'X']+[0], mask.count('X'))}

    def apply(self, addr):
        yield from ((addr | self.or_mask) & self.and_mask | num for num in self.floating_nums)

class MaskInstruction:
    def __init__(self, mask, mask_cls=BitMask):
        self.mask = mask
        self.mask_cls = mask_cls

    def execute(self, program):
        program.mask = self.mask_cls(self.mask)

class MemoryInstruction:
    instruction_pattern = re.compile(r"mem\[(\d+)\] = (\d+)")
    def __init__(self, addr, num):
        self.addr = addr
        self.num = num

    def execute(self, program):
        program.memory[self.addr] = program.mask.apply(self.num)

class FloatingMemoryInstruction:
    instruction_pattern = re.compile(r"mem\[(\d+)\] = (\d+)")
    def __init__(self, addr, num):
        self.addr = addr
        self.num = num

    def execute(self, program):
        for addr in program.mask.apply(self.addr):
            program.memory[addr] = self.num

class Program:
    def __init__(self):
        self.memory = {}
        self.mask = None

    def run(self, instructions):
        for i in instructions:
            i.execute(self)

def parse_input(lines, mask_cls, mem_instruction_cls):
    instructions = []
    for line in lines:
        if line[:3] == "mas":
            mask = line[7:]
            yield MaskInstruction(mask, mask_cls)
        if line[:3] == "mem":
            addr, num = MemoryInstruction.instruction_pattern.fullmatch(line).groups()
            yield mem_instruction_cls(int(addr), int(num))

def part1(lines):
    instructions = parse_input(lines, BitMask, MemoryInstruction)
    p = Program()
    p.run(instructions)
    return sum(p.memory.values())

def part2(lines):
    instructions = parse_input(lines, FloatingBitMask, FloatingMemoryInstruction)
    p = Program()
    p.run(instructions)
    return sum(p.memory.values())

sample1 = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0""".split("\n")
assert_equals(part1(sample1), 165)

sample2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1""".split("\n")
assert_equals(part2(sample2), 208)

sample3 = """mask = 110000011XX0000X101000X10X01XX001011
mem[49397] = 468472""".split("\n")
assert_equals(part2(sample3), 59964416)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines))
print(part2(lines))
