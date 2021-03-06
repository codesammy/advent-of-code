import sys
sys.path.append('../')
from util import read_file_one_string, assert_equals
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Deque
import math

@dataclass
class OpCode:
    intcode: type = field(repr=False)
    parameter_modes: List[int] = field(init=False)

    def __post_init__(self):
        self.parameter_modes = [0, 0, 0]

    def execute(self):
        pass

    def _get_operand_idx(self, i):
        # immediate mode
        idx = self.intcode.ip + i + 1
        if self.parameter_modes[i] == 0:
            # position mode
            idx = self.intcode.memory[self.intcode.ip + i + 1]
        elif self.parameter_modes[i] == 2:
            # relateive mode
            idx = self.intcode.rb + self.intcode.memory[self.intcode.ip + i + 1]
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
    memory: Dict[int, int]
    input: Deque[int] = field(default_factory=deque)
    output: Deque[int] = field(default_factory=deque)
    ip: int = field(init=False, default=0)
    opcodes: Dict[int, OpCode] = field(init=False, default_factory=dict)
    exited: bool = field(init=False, default=False)
    rb: int = field(init=False, default=0)

    def __post_init__(self):
        self.opcodes[1] = OpCode1(self)
        self.opcodes[2] = OpCode2(self)
        if self.input:
            d = deque(self.input)
            self.input = d

    def add_input(self, value):
        self.input.append(value)

    def get_output(self):
        try:
            return self.output.pop()
        except IndexError:
            return None

    def run(self, stop_after=99):
        while value := self.memory[self.ip]:
            opcode_num = value % 100
            if opcode_num == 99:
                self.exited = True
                raise StopIteration
                break
            opcode = self.opcodes[opcode_num]
            opcode.parameter_modes = [value//100%10, value//1000%10, value//10000%10]
            opcode.execute()
            if opcode_num == stop_after:
                break

def parse_input(text):
    return defaultdict(lambda: 0, enumerate(map(int, text.split(','))))

def part1(text, noun=None, verb=None):
    state = parse_input(text)
    if noun and verb:
        state[1] = noun
        state[2] = verb
    program = IntCode(state)
    try:
        program.run()
    except StopIteration:
        pass
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
