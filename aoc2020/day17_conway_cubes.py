import sys
from itertools import takewhile, product
from collections import defaultdict
import re
import math
sys.path.append('../')
from util import read_file, assert_equals

target = (1,2,0)

class Space:
    def __init__(self):
        self.cubes_by_xyz = dict()

    def add(self, x, y, z, active, newcube=False):
        cube = self.cube_at(x, y, z)
        if newcube:
            cube.set_active(active)
        #if h in self.cubes_by_xyz:
        #    if cube.active:
        #        self.cubes_by_xyz[h].set_active(cube.active)
        #else:
        #    # new cube
        #    if (cube.x, cube.y, cube.z) == (0,2,0):
        #        print(f"==== storing cube ref for {cube}")
        #    self.cubes_by_xyz[h] = cube

        # make sure the added cube has all possible neighbors
        for x, y, z in product(range(-1,2), repeat=3):
            cx, cy, cz = cube.x + x, cube.y + y, cube.z + z
            if not (cx == cube.x and cy == cube.y and cz == cube.z):
                c = self.cube_at(cx, cy, cz)
                if (cube.x, cube.y, cube.z) == target:
                    print(f"==== adding neighbor {cube}")
                    pass
                c.neighbors.add(cube)
                if len(c.neighbors) > 26:
                    raise RuntimeError("c had more than 26 neighbors")
                cube.neighbors.add(c)
                if len(cube.neighbors) > 26:
                    raise RuntimeError("cube had more than 26 neighbors")

        return cube

    def parse_input(self, lines):
        z = 0
        for y, row in enumerate(lines):
            for x, cell in enumerate(row):
                self.add(x, y, z, cell=='#', newcube=True)

    def cubes(self):
        return self.cubes_by_xyz.values()

    def cycle(self):
        #print("Cycle")
        snapshot = self.cubes_by_xyz.copy()
        for cube in snapshot.values():
            if cube.active:
                self.add(cube.x, cube.y, cube.z, cube.active, newcube=False)

        snapshot = self.cubes_by_xyz.copy()
        for cube in snapshot.values():
            cube.compute_next()

        for cube in snapshot.values():
            #if not cube.active and cube.next_active:
                #self.add(cube)
            #print(f"setting {cube} from {cube.active} to {cube.next_active}")
            #if cube.z == -2:
                #print(f"setting {cube} to active {self.next_active}")
            cube.evolve()

    def __str__(self):
        res = ""
        xs = {cube.x for cube in self.cubes()}
        ys = {cube.y for cube in self.cubes()}
        zs = {cube.z for cube in self.cubes()}
        for z in range(min(zs), max(zs)+1):
            res += f"z={z}" + "\n"
            for y in range(min(ys), max(ys)+1):
                for x in range(min(xs), max(xs)+1):
                    #print(Cube.hash_xyz2(x,y,z), end=" ")
                    #print(f"{(x,y,z)}")

                    h = Cube.hash_xyz2(x, y, z)
                    if h in self.cubes_by_xyz:
                        cube = self.cubes_by_xyz[h]
                        #if cube.z == -2:
                            #print(f"{cube} has {cube.active_neighbor_count()} n")

                        special = False
                        if (x,y) == (0,0):
                            res += "\033[32;1;m"
                            special = True
                        elif (x,y,z) == target:
                            res += "\033[31;1;m"
                            special = True
                        elif cube in self.cubes_by_xyz[Cube.hash_xyz2(target[0], target[1], target[2])].neighbors:
                            res += "\033[33;1;m"
                            special = True
                        res += "#" if cube.active else "."
                        if special:
                            res += "\033[0m"
                    else:
                        res += " "
                res += "\n"
            res += "\n\n"
        return res

    def cube_at(self, x, y, z):
        h = Cube.hash_xyz2(x, y, z)
        c = None
        if h in self.cubes_by_xyz:
            c = self.cubes_by_xyz[h]
        else:
            #if cz == -2:
            #print(f"{(cx, cy, cz )} cube was created while adding {cube}")
            c = Cube(x, y, z, False)
            #print(f"creating a new neighbor cube {c}")
            self.cubes_by_xyz[h] = c
        return c

    @classmethod
    def create_cube(cls, x, y, z):
        pass

class Cube:
    def __init__(self, x, y, z, active):
        self.x = x
        self.y = y
        self.z = z
        self.active = active
        self.set_active(active)

        self.next_active = None
            #if not self.active:
            #    raise
        self.neighbors = set()

    def compute_next(self):
        active_neighbor_count = self.active_neighbor_count()
        if (self.x, self.y, self.z) == target:
            print(f"{self} has {active_neighbor_count} active neighbors")
            for n in self.neighbors:
                if n.active:
                    print(n)
            print("###")
        if self.active:
            if (active_neighbor_count in [2, 3]):
                self.next_active = self.active
                if (self.x, self.y, self.z) == (2,2,0):
                    print("will stay active!")
            else:
                self.next_active = False
        else:
            if (active_neighbor_count in [3]):
                #print("Willbecomeactive")
                self.next_active = True
            else:
                self.next_active = self.active
        if (self.x, self.y, self.z) == target:
            print(f"-> {self} will become active: {self}")

    def evolve(self):
        if self.next_active != None:
            self.set_active(self.next_active)
        self.next_active = None

    def set_active(self, active):
        if (self.x, self.y, self.z) == target:
            print(f"setting {self} to active {active}")
            if self.active and not active:
                #raise
                pass
        self.active = active

    def active_neighbor_count(self):
        return sum(1 for n in self.neighbors if n.active)

    def __hash__(self):
        return Cube.hash_xyz2(self.x, self.y, self.z)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Cube({self.x},{self.y},{self.z},{self.active})#{id(self)}"

    @classmethod
    def hash_xyz2(cls, x, y, z):
        return 100**2 * z + 100**1 * y + x

def part1(lines):
    space = Space()
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
print("OK")



lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines))
