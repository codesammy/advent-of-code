import sys
sys.path.append('../')
from util import read_file_one_string, assert_equals

from dataclasses import dataclass, field
from typing import List, Set
from collections import defaultdict
import math
import copy
import re
import cProfile

debug = False

@dataclass
class Tile:
    tileId: int
    data: List[str]
    orientation: int  = field(default=0, compare=False)
    flipped_horizontal: bool = field(default=False, compare=False)
    flipped_vertical: bool = field(default=False, compare=False)
    borders: List[type] = field(init=False, repr=False, compare=False)
    corners: List[type] = field(init=False, repr=False, compare=False)
    top_border: str = field(init=False, repr=False, compare=False)
    right_border: str = field(init=False, repr=False, compare=False)
    bottom_border: str = field(init=False, repr=False, compare=False)
    left_border: str = field(init=False, repr=False, compare=False)
    orientations: List[type] = field(init=False, repr=False, compare=False, default=None)

    def __post_init__(self):
        self.borders = list(self.calc_borders())
        self.corners = list(self.calc_corners())

    def calc_orientations(self):
        if self.orientations:
            return self.orientations
        os = [self]
        for fh in [True, False]:
            for fv in [True, False]:
                for orientation in [0,1,2,3]:
                    no = self.calc_orientation(orientation, fh, fv)
                    if no not in os:
                        os.append(no)
        self.orientations = os
        return os

    def calc_orientation(self, orientation, fh, fv):
        new_data = self.data.copy()
        if fh:
            new_data = ["".join(reversed(row)) for row in new_data]
        if fv:
            new_data = list(reversed(new_data))
        def rotate(data):
            res = []
            for column in range(len(data[0])):
                c = "".join(row[column] for row in data)
                res.append(c)
            return res
        for _ in range(orientation):
            new_data = rotate(new_data)
        return Tile(self.tileId, new_data, orientation, fh, fv)

    def calc_corners(self):
        self.top_left = Corner(self, 'top_left', self.top_border, self.left_border)
        self.top_right = Corner(self, 'top_right', self.top_border, self.right_border)
        self.bottom_right = Corner(self, 'bottom_right', self.bottom_border, self.right_border)
        self.bottom_left = Corner(self, 'bottom_left', self.bottom_border, self.left_border)
        return [self.top_left, self.top_right, self.bottom_right, self.bottom_left]

    def calc_borders(self):
        self.top_border = Border(self, self.to_int(self.data[0]))
        self.right_border = Border(self, self.to_int("".join(line[-1] for line in self.data)))
        self.bottom_border = Border(self, self.to_int(self.data[-1]))
        self.left_border = Border(self, self.to_int("".join(line[0] for line in self.data)))
        return [self.top_border, self.right_border, self.bottom_border, self.left_border]

    def to_int(self, text):
        return int(text.translate(str.maketrans({'.':'0', '#':'1'})),2)

    def __str__(self):
        s = "\n".join(self.data)
        return f"Tile {self.tileId} \n" + s

@dataclass
class EmptyTile:
    top_border: str = field(init=False, default=None, repr=False, compare=False)
    right_border: str = field(init=False, default=None, repr=False, compare=False)
    bottom_border: str = field(init=False, default=None, repr=False, compare=False)
    left_border: str = field(init=False, default=None, repr=False, compare=False)
    def __str__(self):
        s = "\n".join(['.'*10]*10)
        return f"Tile EMPTY\n" + s
    
@dataclass(frozen=True)
class Border:
    tile: Tile = field(repr=False, compare=False)
    data: int
    flipped: bool = field(default=False, compare=False)

@dataclass
class Corner:
    tile: Tile = field(repr=False, compare=False)
    name: str
    border1: Border
    border2: Border

    def borders(self):
        return [self.border1, self.border2]
    
def parse_input(text):
    blocks = [[line.strip() for line in block.split('\n')] for block in text.split('\n\n')]
    for block in blocks:
        yield Tile(int(block[0][-5:-1]), block[1:])

@dataclass
class Image:
    size: int
    data: List[List[Tile]] = field(init=False)
    skip: bool = field(default=False)
    tiles: Set[str] = field(init=False, default_factory=set)

    def __post_init__(self):
        data = []
        for _ in range(self.size):
            row = []
            for _ in range(self.size):
                row.append(EmptyTile())
            data.append(row)
        self.data = data

    def __str__(self):
        s = ""
        for tiles in self.data:
            for rows in zip(*map(lambda t: str(t).split("\n"), tiles)):
                s += " ".join(rows) + "\n"
            s += "\n"
        return s

    def deepcopy(self):
        n = Image(self.size)
        nd = [[t for t in rows] for rows in self.data]
        n.data = nd
        return n

    def add(self, x, y, tile):
        self.data[y][x] = tile
        self.tiles.add(tile.tileId)
    
def solve(tiles):
    edge_length = int(math.sqrt(len(tiles)))
    i = Image(edge_length)
    
    images = [i]

    def fits(orientation, top, right, bottom, left):
        top_matches, right_matches, bottom_matches, left_matches = (True, True, True, True)

        if top:
            top_matches = orientation.top_border.data == top.data
        if right:
            right_matches = orientation.right_border == right
        if bottom:
            bottom_matches = orientation.bottom_border == bottom
        if left:
            left_matches = orientation.left_border.data == left.data
        all_match = top_matches and right_matches and bottom_matches and left_matches

        return all_match

    build_candidates_counter = 0
    for y in range(edge_length):
        for x in range(edge_length):
            if debug:
                print(f"Looking for position {x},{y}")
            for idx, image in enumerate((imgs := [i for i in images if not i.skip])):
                if debug:
                    print(f"Trying image {idx+1}/{len(imgs)}")
                    print(image)
                top, right, bottom, left = (None, None, None, None)
                
                if y >= 1:
                    top = image.data[y-1][x].bottom_border
                if x <= edge_length - 2:
                    right = image.data[y][x+1].left_border
                if y <= edge_length - 2:
                    bottom = image.data[y+1][x].top_border
                if x >= 1:
                    left = image.data[y][x-1].right_border

                candidates = [o for t in tiles for o in t.calc_orientations() if t.tileId not in image.tiles and fits(o, top, right, bottom, left)]
                build_candidates_counter += 1

                if debug:
                    print(f"choosing from {len(candidates)} candidates for pos {x}")
                finished = False
                if len(candidates) < 1:
                    if debug:
                        print(f"Can't go on, deleting idx {idx}")
                    image.skip = True
                    continue
                elif len(candidates) == 1:
                    image.add(x, y, candidates[0])
                    if (x,y) == (edge_length - 1, edge_length - 1):
                        if debug:
                            print(image)
                        return image
                elif len(candidates) > 1:
                    c = candidates[0]
                    image.add(x, y, c)
                    for c in candidates[1:]:
                        ni = image.deepcopy()
                        ni.add(x, y, c)
                        if (x, y) == (edge_length - 1, edge_length - 1):
                            if debug:
                                print(ni)
                            return ni
                        if debug:
                            print(f"Branching new possibility at pos {x}")
                        images.append(ni)
                images = [i for i in images if not i.skip]
                if finished:
                    print(f"build_candidates_counter = {build_candidates_counter}")
                    return
    raise RuntimeError("no solution")

def part1(text):
    tiles = list(parse_input(text))
    image = solve(tiles)
    n = image.size - 1
    return math.prod(map(lambda t: image.data[t[0]][t[1]].tileId, [(0,0), (n,0), (0,n), (n,n)]))

def part2(text):
    tiles = list(parse_input(text))
    image = solve(tiles)
    noborders = ""

    for y, row in enumerate(image.data):
        for l in range(1,9):
            for x, tile in enumerate(row):
                noborders += tile.data[l][1:-1]
            noborders += "\n"
    noborders = noborders[:-1]
    
    def search_for_sea_monsters(flipped, rotation, text):
        if flipped:
            text = "\n".join(map(lambda l: "".join(l), map(reversed, text.split("\n"))))
        for i in range(rotation):
            data = text.split("\n")
            res = []
            for column in range(len(data[0])):
                s = ""
                for row in reversed(data):
                    s += row[column]
                res.append(s)
            text = "\n".join(res)

        pixels_per_side = len(text.split("\n")[0])

        water_roughness = sum(1 for line in text.split("\n") for char in line if char == '#')
        sea_monster_count  = 0
        sea_monster_top    = re.compile(r"..................#.")
        sea_monster_middle = re.compile(r"#....##....##....###")
        sea_monster_bottom = re.compile(r".#..#..#..#..#..#...")
        for y in range(0, pixels_per_side - 2):
            for x in range(0, pixels_per_side - 20):
                top    = text.split("\n")[y][x:x+20]
                middle = text.split("\n")[y+1][x:x+20]
                bottom = text.split("\n")[y+2][x:x+20]
                if sea_monster_top.fullmatch(top) and sea_monster_middle.fullmatch(middle) and sea_monster_bottom.fullmatch(bottom):
                    sea_monster_count += 1
        if sea_monster_count:
            water_roughness -= 15 * sea_monster_count
        return sea_monster_count, water_roughness
        
    for fh in [False, True]:
        for rotation in range(4):
            c, r = search_for_sea_monsters(fh, rotation, noborders)
            if c > 0:
                return r

sample1 = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""
assert_equals(part1(sample1), 20899048083289)
assert_equals(part2(sample1), 273)

inputtext = read_file_one_string(sys.argv[0].replace("py", "input"))
print(part1(inputtext))
print(part2(inputtext))
