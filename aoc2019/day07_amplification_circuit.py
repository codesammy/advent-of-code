from collections import defaultdict
from dataclasses import dataclass, field
from itertools import permutations
from pathlib import Path
import re
import sys
from typing import Dict, List
from unittest import TestCase
sys.path.append('.')
from day05_sunny_with_a_chance_of_asteroids import IntCode2, parse_input

def part1(text):
    def run_phases(phases):
        state = parse_input(text)
        program = IntCode2(state, iter([phases[0],0]))
        program.run()
        output = int(program.output)
        program = IntCode2(state, iter([phases[1],output]))
        program.run()
        output = int(program.output)
        program = IntCode2(state, iter([phases[2],output]))
        program.run()
        output = int(program.output)
        program = IntCode2(state, iter([phases[3],output]))
        program.run()
        output = int(program.output)
        program = IntCode2(state, iter([phases[4],output]))
        program.run()
        return int(program.output)

    return max(run_phases(c) for c in permutations(range(5)))

class Test(TestCase):

    def runTest(self):
        sample1 = '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'
        self.assertEqual(part1(sample1), 43210)
        sample1 = '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'
        self.assertEqual(part1(sample1), 54321)
        sample1 = '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'
        self.assertEqual(part1(sample1), 65210)

if __name__ == '__main__' or True:
    Test().debug()
    inputtext = Path(sys.argv[0].replace("py", "input")).read_text()
    # find the largest output signal that can be sent to the thrusters
    print(part1(inputtext))
