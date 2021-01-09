from collections import defaultdict
from dataclasses import dataclass, field
from itertools import combinations, permutations
import math
from operator import itemgetter
from pathlib import Path
import re
import sys
import traceback
from typing import Dict, List
from unittest import TestCase
sys.path.append('.')
from day09_sensor_boost import IntCode3
from day02_1202_program_alarm import OpCode, parse_input

@dataclass
class Vector3:
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def compare(self, other):
        def cmp(a,b):
            if a == b:
                return 0
            elif a > b:
                return -1
            else:
                return 1
        return Vector3(cmp(self.x, other.x), cmp(self.y, other.y), cmp(self.z, other.z))

@dataclass
class Moon:
    pos: Vector3
    vel: Vector3 = field(default=Vector3(0, 0, 0))

    def adjust_gravity(self, other):
        self.vel += self.pos.compare(other.pos)
        other.vel += other.pos.compare(self.pos)

    def move(self):
        self.pos += self.vel

    def potential_energy(self):
        return abs(self.pos.x) + abs(self.pos.y) + abs(self.pos.z)

    def kinetic_energy(self):
        return abs(self.vel.x) + abs(self.vel.y) + abs(self.vel.z)

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()

def parse_input(text):
    for x, y, z in re.findall(r"<x=([^=,]+), y=([^=,]+), z=([^=,]+)>", text):
        yield Moon(Vector3(int(x), int(y), int(z)))

def part1(text, steps):
    moons = list(parse_input(text))
    for i in range(steps):
        for a,b in combinations(moons, 2):
            a.adjust_gravity(b)
        for m in moons:
            m.move()
    return sum(m.total_energy() for m in moons)

class Test(TestCase):

    def runTest(self):
        sample = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""
        self.assertEqual(part1(sample, 10), 179)

if __name__ == '__main__' or True:
    Test().debug()
    inputtext = Path(sys.argv[0].replace("py", "input")).read_text().strip()
    # What is the total energy in the system after simulating the moons given in your scan for 1000 steps?
    print(part1(inputtext, 1000))
