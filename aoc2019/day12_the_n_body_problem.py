from collections import defaultdict
from dataclasses import dataclass, field
from itertools import combinations, permutations, starmap
import math
from operator import eq, itemgetter
from pathlib import Path
import re
import sympy
import sys
import traceback
from typing import Dict, List
from unittest import TestCase

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

def step(moons):
    for a,b in combinations(moons, 2):
        a.adjust_gravity(b)
    for m in moons:
        m.move()

def part1(text, steps):
    moons = list(parse_input(text))
    for i in range(steps):
        step(moons)
    return sum(m.total_energy() for m in moons)

def part2(text):
    initial_moons = list(parse_input(text))
    moons = list(parse_input(text))
    steps = 0
    x_rep, y_rep, z_rep = None, None, None
    while True:
        step(moons)
        steps += 1
        if not x_rep and all(starmap(eq, zip([(m.pos.x, m.vel.x) for m in initial_moons], [(m.pos.x, m.vel.x) for m in moons]))):
            x_rep = steps
        if not y_rep and all(starmap(eq, zip([(m.pos.y, m.vel.y) for m in initial_moons], [(m.pos.y, m.vel.y) for m in moons]))):
            y_rep = steps
        if not z_rep and all(starmap(eq, zip([(m.pos.z, m.vel.z) for m in initial_moons], [(m.pos.z, m.vel.z) for m in moons]))):
            z_rep = steps
        if x_rep and y_rep and z_rep:
            break

    all_factors = sympy.factorint(x_rep*y_rep*z_rep).keys()
    # only keep max exp of all prime factor bases
    return math.prod(map(lambda f: f**max(sympy.factorint(x_rep).get(f, 0), sympy.factorint(y_rep).get(f, 0), sympy.factorint(z_rep).get(f, 0)), all_factors))

class Test(TestCase):

    def runTest(self):
        sample = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""
        self.assertEqual(part1(sample, 10), 179)
        sample = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""
        self.assertEqual(part2(sample), 2772)
        sample = """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""
        self.assertEqual(part2(sample), 4686774924)

if __name__ == '__main__' or True:
    Test().debug()
    inputtext = Path(sys.argv[0].replace("py", "input")).read_text().strip()
    # What is the total energy in the system after simulating the moons given in your scan for 1000 steps?
    print(part1(inputtext, 1000))
    print(part2(inputtext))
