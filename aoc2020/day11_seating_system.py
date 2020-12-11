import sys
sys.path.append('../')
from util import read_file, assert_equals
from itertools import product

def cell_factory(x, y, c, cls):
    cell = None
    if c == "#" or c == "L":
        cell = cls(x, y, c)
    else:
        cell = Floor(x, y, c)
    return cell

class Cell:
    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.c = c
        self.occupied = False

    def link(self, grid):
        pass

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "!"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.c == other.c

class Seat(Cell):
    def __init__(self, x, y, c):
        super(Seat, self).__init__(x, y, c)
        self.compute()

    def compute(self):
        self.occupied = self.c == "#"

    def link(self, grid):
        self.grid = grid
        self.neighbors = [cell for x, y in product(range(-1,2), repeat=2) if (cell := grid.at(self.x + x, self.y + y)) and cell != self]

    def next(self):
        c = "?"
        if not self.occupied and all(map(lambda c: c.occupied == False, self.neighbors)):
            c = "#"
        elif self.occupied and sum((1 if c.occupied else 0 for c in self.neighbors )) >= 4:
            c = "L"
        else:
            c = self.c
        self.next_c = c
        return c

    def evolve(self):
        self.c = self.next_c
        self.compute()
        return self

    def __str__(self):
        return "#" if self.occupied else "L"

class SeatWithFarNeighbors(Seat):
    def link(self, grid):
        self.grid = grid
        self.neighbors = []
        for x, y in product(range(-1,2), repeat=2):
            if not (x == 0 and y == 0):
                if (cell := grid.at(self.x + x, self.y + y)) and isinstance(cell, type(self)):
                    self.neighbors.append(cell)
                else:
                    i = 2
                    while True:
                        fx = x * i
                        fy = y * i
                        if self.x + fx in range(grid.width) and self.y + fy in range(grid.height):
                            cell = grid.at(self.x + fx, self.y + fy)
                            if isinstance(cell, type(self)):
                                self.neighbors.append(cell)
                                break
                        else:
                            break
                        i += 1

    def next(self):
        c = "?"
        if not self.occupied and all(map(lambda c: c.occupied == False, self.neighbors)):
            c = "#"
        elif self.occupied and sum((1 if c.occupied else 0 for c in self.neighbors )) >= 5:
            c = "L"
        else:
            c = self.c
        self.next_c = c
        return c

class Floor(Cell):
    def __init__(self, x, y, c):
        super(Floor, self).__init__(x, y, c)

    def next(self):
        return self.c

    def evolve(self):
        return self

    def __str__(self):
        return "."

class Grid:
    def __init__(self, rows, cls):
        self.width = len(rows[0])
        self.height = len(rows)
        self.rows = [[cell_factory(x, y, cell, cls) for x, cell in enumerate(row)] for y, row in enumerate(rows)]
        self.link()

    def link(self):
        for row in self.rows:
            for cell in row:
                cell.link(self)

    def at(self, x, y, rows=None):
        if not rows:
            rows = self.rows
        ret = None
        if x in range(self.width) and y in range(self.height):
            ret = rows[y][x]
        return ret

    def simulate(self):
        while True:
            def changed(old, new):
                for y, row in enumerate(self.rows):
                    for x, cell in enumerate(row):
                        if old[y][x] != new[y][x]:
                            return True
                return False
            old_cellstate = [[cell.c for cell in row] for row in self.rows]
            new_cellstate = [[cell.next() for cell in row] for row in self.rows]

            if not changed(old_cellstate, new_cellstate):
                return

            for row in self.rows:
                for cell in row:
                    cell.evolve()

    def count_seats(self):
        return sum((1 for row in self.rows for cell in row if cell.occupied))

    def __str__(self):
        return "\n".join(map(lambda row: "".join([str(cell) for cell in row]), self.rows))

def part1(rows):
    grid = Grid(rows, Seat)
    grid.simulate()
    return grid.count_seats()

def part2(rows):
    grid = Grid(rows, SeatWithFarNeighbors)
    grid.simulate()
    return grid.count_seats()

sample1 = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".split("\n")
assert_equals(part1(sample1), 37)
assert_equals(part2(sample1), 26)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines))
print(part2(lines))
