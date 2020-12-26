import sys
dir(sys)
sys.path.append('..')
sys.path.append('.')
from util import read_file_one_string, assert_equals
from day02_1202_program_alarm import OpCode, IntCode

from dataclasses import dataclass, field
from typing import Dict, List
import math

class OpCode3(OpCode):
    def execute(self):
        result = next(self.intcode.input)
        self.set_operand(0, result)
        self.intcode.ip += 2

class OpCode4(OpCode):
    def execute(self):
        result = self.get_operand(0)
        self.intcode.output += str(result)
        self.intcode.ip += 2

def parse_input(text):
    return list(map(int, text.split(',')))

def part1(text, input=[]):
    state = parse_input(text)
    program = IntCode(state, iter(input))
    program.opcodes[3] = OpCode3(program)
    program.opcodes[4] = OpCode4(program)
    program.run()
    return program.output

assert_equals(part1("3,0,4,0,99", [300]), "300")
assert_equals(part1("1002,4,3,4,33", [1]), "")
assert_equals(part1("1101,100,-1,4,0", [1]), "")

inputtext = read_file_one_string(sys.argv[0].replace("py", "input"))
print(part1(inputtext, [1]))
