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

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def angle(self, asteroid):
        vec = self.to(asteroid)

        # transform to typical coordinate system vector
        vec = Point(vec.x, -vec.y)
        return (math.atan2(vec.x, vec.y)*180)/math.pi+(360*(vec.x < 0))

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
    candidate = None
    for asteroid in grid:
        num = visible_other_asteroids(grid, asteroid)
        if num > maximum:
            candidate = asteroid
            maximum = num
    return maximum

def part2(text, station):
    grid = list(parse_input(text))
    asteroids = [(station.angle(a), a) for a in grid if a != station]
    asteroids = sorted(asteroids, key=itemgetter(0))
    eliminated_asteroid_count = 0
    while eliminated_asteroid_count < 200:
        to_be_deleted = []
        for i, (ang, ast) in enumerate(asteroids):
            if ast.is_in_line_of_sight(station, [o for _, o in asteroids if o != ast]):
                # elimination
                eliminated_asteroid_count += 1
                if eliminated_asteroid_count == 200:
                    return ast.x * 100 + ast.y
                to_be_deleted.append(i)
        for i in to_be_deleted:
            del(asteroids[i])

class Test(TestCase):

    def runTest(self):
        self.assertEqual(Point(0,0).angle(Point(0, -4)), 0)
        self.assertEqual(Point(0,0).angle(Point(4, -4)), 45)
        self.assertEqual(Point(0,0).angle(Point(4, 0)), 90)
        self.assertEqual(Point(0,0).angle(Point(4, 4)), 135)
        self.assertEqual(Point(0,0).angle(Point(0, 4)), 180)
        self.assertEqual(Point(0,0).angle(Point(-4, 4)), 225)
        self.assertEqual(Point(0,0).angle(Point(-4, 0)), 270)
        self.assertEqual(Point(0,0).angle(Point(-4, -4)), 315)
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
        sample = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
        self.assertEqual(part2(sample, Point(11,13)), 802)

if __name__ == '__main__':
    Test().debug()
    inputtext = Path(sys.argv[0].replace("py", "input")).read_text().strip()
    # Find the best location for a new monitoring station.
    # How many other_reduced asteroids can be detected from that location?
    print(part1(inputtext))
    print(part2(inputtext, Point(17,23)))
