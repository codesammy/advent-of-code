from collections import defaultdict
from dataclasses import dataclass, field
from itertools import permutations
from operator import itemgetter
from pathlib import Path
import traceback
import re
import sys
from typing import Dict, List
from unittest import TestCase
sys.path.append('.')
from day05_sunny_with_a_chance_of_asteroids import IntCode2
from day02_1202_program_alarm import OpCode, parse_input

class OpCode9(OpCode):
    def execute(self):
        value = self.get_operand(0)
        self.intcode.rb += value
        self.intcode.ip += 2

class IntCode3(IntCode2):
    def __post_init__(self):
        super().__post_init__()
        self.opcodes[9] = OpCode9(self)

def part1(text, input):
    state = parse_input(text)
    try:
        program = IntCode3(state, input)
        program.run()
    except StopIteration as e:
        pass
    return ",".join(map(str, list(program.output)))

part2 = part1

class Test(TestCase):

    def runTest(self):
        sample = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
        self.assertEqual(part1(sample, []), sample)
        self.assertEqual(part1("1102,34915192,34915192,7,4,7,99,0", []), "1219070632396864")
        self.assertEqual(part1("104,1125899906842624,99", []), "1125899906842624")

if __name__ == '__main__' or True:
    Test().debug()
    inputtext = Path(sys.argv[0].replace("py", "input")).read_text().strip()
    # find the layer that contains the fewest 0 digits
    # On that layer, what is the number of 1 digits multiplied by the number of 2 digits?
    print(part1(inputtext, [1]))
    print(part2(inputtext, [2]))
