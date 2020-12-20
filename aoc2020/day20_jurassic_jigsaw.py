import sys
sys.path.append('../')
from util import read_file_one_string, assert_equals

from dataclasses import dataclass, field
from typing import List
from collections import Counter
import math

@dataclass
class Tile:
    tileId: int
    data: List[str]
    orientation: int  = field(default=0)
    flipped_horizontal: bool = field(default=False)
    flipped_vertical: bool = field(default=False)
    borders: List[type] = field(init=False, repr=False)
    corners: List[type] = field(init=False, repr=False)
    top_border: str = field(init=False, repr=False)
    right_border: str = field(init=False, repr=False)
    bottom_border: str = field(init=False, repr=False)
    left_border: str = field(init=False, repr=False)

    def __post_init__(self):
        if self.orientation == 0 and not self.flipped_horizontal and not self.flipped_vertical:
            self.orientations = list(self.calc_orientations())

        self.borders = list(self.calc_borders())
        self.corners = list(self.calc_corners())

    def calc_orientations(self):
        for fh in [True, False]:
            for fv in [True, False]:
                for orientation in range(3):
                    if not (orientation == self.orientation and fh == self.flipped_horizontal and fv == self.flipped_vertical):
                        yield self.calc_orientation(orientation, fh, fv)

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
        self.top_border = Border(self, self.data[0])
        self.right_border = Border(self, "".join(line[-1] for line in self.data))
        self.bottom_border = Border(self, self.data[-1])
        self.left_border = Border(self, "".join(line[0] for line in self.data))
        return [self.top_border, self.right_border, self.bottom_border, self.left_border]

    def __str__(self):
        s = "\n".join(self.data)
        return f"Tile {self.tileId}\n" + s

@dataclass
class Border:
    tile: Tile = field(repr=False, compare=False)
    data: str = field(hash=True)
    flipped: bool = field(default=False, compare=False)

    def variants(self):
        variants = [self]
        rev = "".join(reversed(self.data))
        if rev != self.data:
            variants.append(Border(self.tile, rev, True))
        return variants

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

def part1(text):
    tiles = list(parse_input(text))
    
    def matching_borders(border):
        other_tiles = [tile for tile in tiles if tile.tileId != border.tile.tileId]
        other_borders = [b for t in other_tiles for o in t.orientations for b in o.borders]
        return list(ob for ob in other_borders if ob.data == border.data)

    # a corner that can't be matched with any other border of other tile orientations
    corner_candidates = [corner for tile in tiles for orientation in tile.orientations for corner in orientation.corners if tuple(map(len, map(matching_borders, corner.borders()))) == (0, 0)]

    corner_tiles = {corner.tile.tileId for corner in corner_candidates}
    return math.prod(corner_tiles)

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

inputtext = read_file_one_string(sys.argv[0].replace("py", "input"))
print(part1(inputtext))
