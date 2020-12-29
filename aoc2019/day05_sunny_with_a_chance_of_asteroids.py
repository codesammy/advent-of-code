import sys
sys.path.append('..')
sys.path.append('.')
from util import read_file_one_string, assert_equals
from day02_1202_program_alarm import OpCode, IntCode

from dataclasses import dataclass, field
from typing import Dict, List
import math

class OpCode3(OpCode):
    def execute(self):
        value = self.intcode.input.popleft()
        self.set_operand(0, value)
        self.intcode.ip += 2

class OpCode4(OpCode):
    def execute(self):
        value = self.get_operand(0)
        self.intcode.output.append(value)
        self.intcode.ip += 2

class OpCode5(OpCode):
    def execute(self):
        value = self.get_operand(0)
        target = self.get_operand(1)
        if value != 0:
            self.intcode.ip = target
        else:
            self.intcode.ip += 3

class OpCode6(OpCode):
    def execute(self):
        value = self.get_operand(0)
        target = self.get_operand(1)
        if value == 0:
            self.intcode.ip = target
        else:
            self.intcode.ip += 3

class OpCode7(OpCode):
    def execute(self):
        value1 = self.get_operand(0)
        value2 = self.get_operand(1)
        self.set_operand(2, int(value1 < value2))
        self.intcode.ip += 4

class OpCode8(OpCode):
    def execute(self):
        value1 = self.get_operand(0)
        value2 = self.get_operand(1)
        self.set_operand(2, int(value1 == value2))
        self.intcode.ip += 4

class IntCode2(IntCode):
    def __post_init__(self):
        super().__post_init__()
        self.opcodes[3] = OpCode3(self)
        self.opcodes[4] = OpCode4(self)
        self.opcodes[5] = OpCode5(self)
        self.opcodes[6] = OpCode6(self)
        self.opcodes[7] = OpCode7(self)
        self.opcodes[8] = OpCode8(self)

def parse_input(text):
    return list(map(int, text.split(',')))

def part1(text, input=[]):
    state = parse_input(text)
    program = IntCode(state, iter(input))
    program.opcodes[3] = OpCode3(program)
    program.opcodes[4] = OpCode4(program)
    try:
        program.run()
    except StopIteration:
        pass
    return program.get_output()

def part2(text, input=[]):
    state = parse_input(text)
    program = IntCode2(state, iter(input))
    try:
        program.run()
    except StopIteration:
        pass
    return program.get_output()

if __name__ == '__main__':
    assert_equals(part1("3,0,4,0,99", [300]), 300)
    assert_equals(part1("1002,4,3,4,33", [1]), None)
    assert_equals(part1("1101,100,-1,4,0", [1]), None)

    assert_equals(part2("3,9,8,9,10,9,4,9,99,-1,8", [7]), 0)
    assert_equals(part2("3,9,8,9,10,9,4,9,99,-1,8", [8]), 1)
    assert_equals(part2("3,9,8,9,10,9,4,9,99,-1,8", [9]), 0)

    assert_equals(part2("3,9,7,9,10,9,4,9,99,-1,8", [7]), 1)
    assert_equals(part2("3,9,7,9,10,9,4,9,99,-1,8", [8]), 0)

    assert_equals(part2("3,3,1108,-1,8,3,4,3,99", [7]), 0)
    assert_equals(part2("3,3,1108,-1,8,3,4,3,99", [8]), 1)
    assert_equals(part2("3,3,1108,-1,8,3,4,3,99", [9]), 0)

    assert_equals(part2("3,3,1107,-1,8,3,4,3,99", [7]), 1)
    assert_equals(part2("3,3,1107,-1,8,3,4,3,99", [8]), 0)

    assert_equals(part2("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", [0]), 0)
    assert_equals(part2("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", [1]), 1)
    assert_equals(part2("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", [0]), 0)
    assert_equals(part2("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", [1]), 1)

    assert_equals(part2("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", [7]), 999)
    assert_equals(part2("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", [8]), 1000)
    assert_equals(part2("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", [9]), 1001)

    inputtext = read_file_one_string(sys.argv[0].replace("py", "input"))
    print(part1(inputtext, [1]))
    print(part2(inputtext, [5]))
