import sys
sys.path.append('../')
from util import read_file_one_string, assert_equals

from dataclasses import dataclass, field
from typing import Dict, List
import math

class OpCode:
    def execute(self, intcode):
        pass

class OpCode1(OpCode):
    def execute(self, intcode):
        operand1 = intcode.memory[intcode.memory[intcode.ip + 1]]
        operand2 = intcode.memory[intcode.memory[intcode.ip + 2]]
        output_idx = intcode.memory[intcode.ip + 3]
        result = operand1 + operand2
        intcode.memory[output_idx] = result
        intcode.ip += 4

class OpCode2(OpCode):
    def execute(self, intcode):
        operand1 = intcode.memory[intcode.memory[intcode.ip + 1]]
        operand2 = intcode.memory[intcode.memory[intcode.ip + 2]]
        output_idx = intcode.memory[intcode.ip + 3]
        result = operand1 * operand2
        intcode.memory[output_idx] = result
        intcode.ip += 4

@dataclass
class IntCode:
    memory: List[int]
    ip: int = field(default=0)
    opcodes: Dict[int, OpCode] = field(default_factory=dict)

    def __post_init__(self):
        self.opcodes[1] = OpCode1()
        self.opcodes[2] = OpCode2()

    def run(self):
        while (opcode_num := self.memory[self.ip]) != 99:
            opcode = self.opcodes[opcode_num]
            opcode.execute(self)

def parse_input(text):
    return list(map(int, text.split(',')))

def part1(text, noun=None, verb=None):
    state = parse_input(text)
    if noun and verb:
        state[1] = noun
        state[2] = verb
    program = IntCode(state)
    program.run()
    return program.memory[0]

def part2(text):
    for noun in range(100):
        for verb in range(100):
            result = part1(text, noun, verb)
            if result == 19690720:
                return 100*noun+verb

sample = "1,9,10,3,2,3,11,0,99,30,40,50"
assert_equals(part1(sample), 3500)

inputtext = read_file_one_string(sys.argv[0].replace("py", "input"))
print(part1(inputtext, 12, 2))
print(part2(inputtext))
