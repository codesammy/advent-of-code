import sys
from itertools import product, starmap
from operator import add
import re
import math
sys.path.append('../')
from util import read_file, assert_equals

# highlights the cube and its neighbors in the output
target = (0,1,0,0)

class Space:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.cubes_by_xyz = dict()

    def add(self, dims, active, newcube=False):
        cube = self.cube_at(dims)
        if newcube:
            cube.set_active(active)

        # make sure the added cube has all possible neighbors
        for idims in product(range(-1,2), repeat=self.dimensions):
            cdims = tuple(starmap(add, zip(cube.dims, idims)))
            c = self.cube_at(cdims)
            if c != cube:
                c.neighbors.add(cube)
                cube.neighbors.add(c)
        return cube

    def parse_input(self, lines):
        dims = (0,)*self.dimensions
        for y, row in enumerate(lines):
            for x, cell in enumerate(row):
                self.add(((x, y) + dims)[:self.dimensions], cell=='#', newcube=True)

    def cubes(self):
        return self.cubes_by_xyz.values()

    def cycle(self):
        snapshot = self.cubes_by_xyz.copy()
        for cube in snapshot.values():
            if cube.active:
                self.add(cube.dims, cube.active, newcube=False)

        snapshot = self.cubes_by_xyz.copy()
        for cube in snapshot.values():
            cube.compute_next()

        for cube in snapshot.values():
            cube.evolve()

    def __str__(self):
        res = ""
        xs = {cube.dims[0] for cube in self.cubes()}
        ys = {cube.dims[1] for cube in self.cubes()}
        zs = {cube.dims[2:] for cube in self.cubes()}

        for z in zs:
            res += f"z={z}" + "\n"
            for y in range(min(ys), max(ys)+1):
                for x in range(min(xs), max(xs)+1):
                    h = Cube.hash_xyz2((x, y, *z))
                    if h in self.cubes_by_xyz:
                        cube = self.cubes_by_xyz[h]
                        special = False
                        if (x,y) == (0,0):
                            res += "\033[0;32m"
                            special = True
                        elif (x,y,z) == target:
                            res += "\033[0;31m"
                            special = True
                        elif cube in self.cubes_by_xyz[Cube.hash_xyz2(target)].neighbors:
                            res += "\033[0;33m"
                            special = True
                        res += "#" if cube.active else "."
                        if special:
                            res += "\033[0m"
                    else:
                        res += " "
                res += "\n"
            res += "\n\n"
        return res

    def cube_at(self, dims):
        h = Cube.hash_xyz2(dims)
        c = None
        if h in self.cubes_by_xyz:
            c = self.cubes_by_xyz[h]
        else:
            c = Cube(dims, False)
            self.cubes_by_xyz[h] = c
        return c

class Cube:
    def __init__(self, dims, active):
        self.dims = dims
        self.active = active
        self.set_active(active)
        self.next_active = None
        self.neighbors = set()

    def compute_next(self):
        active_neighbor_count = self.active_neighbor_count()
        if self.active:
            if (active_neighbor_count in [2, 3]):
                self.next_active = self.active
            else:
                self.next_active = False
        else:
            if (active_neighbor_count in [3]):
                self.next_active = True
            else:
                self.next_active = self.active

    def evolve(self):
        if self.next_active != None:
            self.set_active(self.next_active)
        self.next_active = None

    def set_active(self, active):
        self.active = active

    def active_neighbor_count(self):
        return sum(1 for n in self.neighbors if n.active)

    def __hash__(self):
        return Cube.hash_xyz2(self.dims)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Cube({self.dims},{self.active})#{id(self)}"

    @classmethod
    def hash_xyz2(cls, dims):
        return sum((100**i*d for i,d in enumerate(reversed(dims))))

def part1(lines):
    space = Space(3)
    space.parse_input(lines)
    print(space)
    for i in range(6):
        print(f"After {i+1} cycle:", end="\n\n")
        space.cycle()
        print(space)
    return sum(1 for cube in space.cubes() if cube.active)

def part2(lines):
    space = Space(4)
    space.parse_input(lines)
    print(space)
    for i in range(6):
        print(f"After {i+1} cycle:", end="\n\n")
        space.cycle()
        print(space)
    return sum(1 for cube in space.cubes() if cube.active)

sample1 = """.#.
..#
###""".split("\n")
assert_equals(part1(sample1), 112)
assert_equals(part2(sample1), 848)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines))
print(part2(lines))
