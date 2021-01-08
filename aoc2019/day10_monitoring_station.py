from collections import defaultdict
from dataclasses import dataclass, field
from itertools import permutations
import math
from operator import itemgetter
from pathlib import Path
import re
import sys
import traceback
from typing import Dict, List
from unittest import TestCase

@dataclass
class Point:
    x: int
    y: int

    def is_in_line_of_sight(self, source, others):
        vector = source.to(self)
        unit_vector = vector.unit()

        if vector == unit_vector:
            return True

        f = 0
        if unit_vector.x == 0:
            f = vector.y // unit_vector.y
        else:
            f = vector.x // unit_vector.x
        for i in range(f):
            in_between = Point(source.x + unit_vector.x * i, source.y + unit_vector.y * i)
            if in_between in others:
                return False

        return True

    def unit(self):
        gcd = math.gcd(self.x, self.y)
        if gcd <= 1:
            return self
        return Point(self.x//gcd, self.y//gcd)

    def to(self, target):
        return Point(target.x - self.x, target.y - self.y)

def parse_input(text):
    for y, row in enumerate(text.split("\n")):
        for x, cell in enumerate(row):
            if cell == '#':
                yield Point(x, y)

def visible_other_asteroids(grid, asteroid):
    others = [a for a in grid if a != asteroid]
    num = len(others)
    for i, other in enumerate(others):
        if not other.is_in_line_of_sight(asteroid, [o for o in others if o != other]):
            num -= 1
    return num

def part1(text):
    grid = list(parse_input(text))
    maximum = 0
    for asteroid in grid:
        num = visible_other_asteroids(grid, asteroid)
        if num > maximum:
            print
            maximum = num
    return maximum

class Test(TestCase):

    def runTest(self):
        sample = """.#..#
.....
#####
....#
...##"""
        self.assertEqual(part1(sample), 8)
        sample = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""
        self.assertEqual(part1(sample), 33)
        sample = """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###."""
        self.assertEqual(part1(sample), 35)
        sample = """.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#.."""
        self.assertEqual(part1(sample), 41)

if __name__ == '__main__':
    Test().debug()
    inputtext = Path(sys.argv[0].replace("py", "input")).read_text().strip()
    # Find the best location for a new monitoring station.
    # How many other_reduced asteroids can be detected from that location?
    print(part1(inputtext))
