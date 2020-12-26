import sys
sys.path.append('../')
from util import read_file_one_string, assert_equals

from dataclasses import dataclass, field
from typing import Dict, Iterable, List
import math

@dataclass
class OpCode:
    intcode: type
    parameter_modes: List[int] = field(init=False)

    def execute(self):
        pass

    def _get_operand_idx(self, i):
        # immediate mode
        idx = self.intcode.ip + i + 1
        if self.parameter_modes[i] == 0:
            # position mode
            idx = self.intcode.memory[self.intcode.ip + i + 1]
        return idx

    def get_operand(self, i):
        return self.intcode.memory[self._get_operand_idx(i)]

    def set_operand(self, i, value):
        self.intcode.memory[self._get_operand_idx(i)] = value

class OpCode1(OpCode):
    def execute(self):
        operand1 = self.get_operand(0)
        operand2 = self.get_operand(1)
        result = operand1 + operand2
        self.set_operand(2, result)
        self.intcode.ip += 4

class OpCode2(OpCode):
    def execute(self):
        operand1 = self.get_operand(0)
        operand2 = self.get_operand(1)
        result = operand1 * operand2
        self.set_operand(2, result)
        self.intcode.ip += 4

@dataclass
class IntCode:
    memory: List[int]
    input: Iterable = field(default_factory=list)
    ip: int = field(init=False, default=0)
    opcodes: Dict[int, OpCode] = field(init=False, default_factory=dict)
    output: str = field(init=False, default="")

    def __post_init__(self):
        self.opcodes[1] = OpCode1(self)
        self.opcodes[2] = OpCode2(self)

    def run(self):
        while (value := self.memory[self.ip]) != 99:
            opcode_num = value % 100
            opcode = self.opcodes[opcode_num]
            opcode.parameter_modes = [value//100%10, value//1000%10, value//10000%10]
            opcode.execute()

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

if __name__ == "__main__":
    sample = "1,9,10,3,2,3,11,0,99,30,40,50"
    assert_equals(part1(sample), 3500)

    inputtext = read_file_one_string(sys.argv[0].replace("py", "input"))
    print(part1(inputtext, 12, 2))
    print(part2(inputtext))
