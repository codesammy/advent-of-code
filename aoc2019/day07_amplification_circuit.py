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

def run_phases(state, phases):
    try:
        program = IntCode2(state, iter([phases[0], 0]))
        program.run(4)
        program = IntCode2(state, iter([phases[1], program.get_output()]))
        program.run(4)
        program = IntCode2(state, iter([phases[2], program.get_output()]))
        program.run(4)
        program = IntCode2(state, iter([phases[3], program.get_output()]))
        program.run(4)
        program = IntCode2(state, iter([phases[4], program.get_output()]))
        program.run(4)
    finally:
        return program.get_output()

def part1(text):
    state = parse_input(text)
    return max(run_phases(state, c) for c in permutations(range(5)))

def part2(text):
    state = parse_input(text)

    def run_phases_feedback(phases):
        adapter1 = IntCode2(state.copy(), (phases[0],))
        adapter2 = IntCode2(state.copy(), (phases[1],))
        adapter3 = IntCode2(state.copy(), (phases[2],))
        adapter4 = IntCode2(state.copy(), (phases[3],))
        adapter5 = IntCode2(state.copy(), (phases[4],))
        last_adapter5_output = 0
        while True:
            try:
                adapter1.add_input(last_adapter5_output)
                adapter1.run(4)
                adapter2.add_input(adapter1.get_output())
                adapter2.run(4)
                adapter3.add_input(adapter2.get_output())
                adapter3.run(4)
                adapter4.add_input(adapter3.get_output())
                adapter4.run(4)
                adapter5.add_input(adapter4.get_output())
                adapter5.run(4)
                last_adapter5_output = adapter5.get_output()
            except StopIteration:
                break
        return last_adapter5_output
    return max(run_phases_feedback(c) for c in permutations(range(5,10)))

class Test(TestCase):

    def runTest(self):
        sample = '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'
        self.assertEqual(part1(sample), 43210)
        sample = '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'
        self.assertEqual(part1(sample), 54321)
        sample = '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'
        self.assertEqual(part1(sample), 65210)
        sample = '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'
        self.assertEqual(part2(sample), 139629729)
        sample = '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'
        self.assertEqual(part2(sample), 18216)

if __name__ == '__main__' or True:
    Test().debug()
    inputtext = Path(sys.argv[0].replace("py", "input")).read_text()
    # find the largest output signal that can be sent to the thrusters
    print(part1(inputtext))
    print(part2(inputtext))
