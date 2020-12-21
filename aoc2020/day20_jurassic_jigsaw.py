import sys
sys.path.append('../')
from util import read_file_one_string, assert_equals

from dataclasses import dataclass, field
from typing import List
from collections import Counter
import math
import copy
import re

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

    def __post_init__(self):
        #if self.orientation == 0 and not self.flipped_horizontal and not self.flipped_vertical:
        #    self.orientations = list(self.calc_orientations())

        self.borders = list(self.calc_borders())
        self.corners = list(self.calc_corners())

    def calc_orientations(self):
        os = [self]
        for fh in [True, False]:
            for fv in [True, False]:
                for orientation in [0,1,2,3]:
                    no = self.calc_orientation(orientation, fh, fv)
                    if no not in os:
                        os.append(no)
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
        self.top_border = Border(self, self.data[0])
        self.right_border = Border(self, "".join(line[-1] for line in self.data))
        self.bottom_border = Border(self, self.data[-1])
        self.left_border = Border(self, "".join(line[0] for line in self.data))
        return [self.top_border, self.right_border, self.bottom_border, self.left_border]

    def __str__(self):
        s = "\n".join(self.data)
        return f"Tile {self.tileId} \n" + s

class EmptyTile:
    def __str__(self):
        s = "\n".join(['.'*10]*10)
        return f"Tile EMPTY\n" + s
    
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

def matching_borders(border, tiles):
    other_tiles = [tile for tile in tiles if tile.tileId != border.tile.tileId]
    other_borders = [b for t in other_tiles for o in t.calc_orientations() for b in o.borders]
    return list(ob for ob in other_borders if ob.data == border.data)

def corner_tiles(tiles):
    # a corner that can't be matched with any other border of other tile orientations
    corner_candidates = [corner for tile in tiles for orientation in tile.calc_orientations() for corner in orientation.corners if tuple(map(len, map(lambda b: matching_borders(b, tiles), corner.borders()))) == (0, 0)]

    return {corner.tile.tileId for corner in corner_candidates}

def part1(text):
    tiles = list(parse_input(text))
    corners = corner_tiles(tiles)
    return math.prod(corners)

@dataclass
class Image:
    size: int
    data: List[List[Tile]] = field(init=False)
    skip: bool = field(default=False)

    def __post_init__(self):
        data = []
        for _ in range(self.size):
            row = []
            for _ in range(self.size):
                row.append(EmptyTile())
            data.append(row)
        self.data = data

    def tiles(self):
        return [tile for rows in self.data for tile in rows if not isinstance(tile, EmptyTile)]

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
        
# step 1 - find corners
# step 2 - find frame
# sept 3 - fill frame
def part2(text):
    tiles = list(parse_input(text))
    # speed boost while dev
    # corner_tile_ids = corner_tiles(tiles)
    # #corner_tile_ids = {2713, 1063, 2749, 1487}
    # corner_tile_objs = [t for t in tiles if t.tileId in corner_tile_ids]
    # print(corner_tile_objs)
    # top_left_candidates = [orientation for tile in corner_tile_objs for orientation in tile.calc_orientations() if tuple(map(len, map(lambda b: matching_borders(b, tiles), orientation.top_left.borders()))) == (0, 0)]
    # top_right_candidates = [orientation for tile in corner_tile_objs for orientation in tile.calc_orientations() if tuple(map(len, map(lambda b: matching_borders(b, tiles), orientation.top_right.borders()))) == (0, 0)]
    # bottom_right_candidates = [orientation for tile in corner_tile_objs for orientation in tile.calc_orientations() if tuple(map(len, map(lambda b: matching_borders(b, tiles), orientation.bottom_right.borders()))) == (0, 0)]
    # bottom_left_candidates = [orientation for tile in corner_tile_objs for orientation in tile.calc_orientations() if tuple(map(len, map(lambda b: matching_borders(b, tiles), orientation.bottom_left.borders()))) == (0, 0)]
    #                         #    bottom_right_candidates = [tile.bottom_right for tile in corner_tile_objs for orientation in tile.calc_orientations()]
    #                         #    bottom_left_candidates = [tile.bottom_left for tile in corner_tile_objs for orientation in tile.calc_orientations()]

    

    edge_length = int(math.sqrt(len(tiles)))
    i = Image(edge_length)
    
    #print(top_left_candidates)
    #i.data[0][0] = top_left
    #top_right = [c for c in top_right_candidates if c.tileId not in map(lambda t: t.tileId, i.tiles())][0]
    #i.data[0][-1] = top_right
    
    #looking_for_n_tiles = edge_length - 2
    images = [i]

    def fits(orientation, top, right, bottom, left):
        top_matches, right_matches, bottom_matches, left_matches = (True, True, True, True)
        #print(top, right, bottom, left)
        if top and not isinstance(top, EmptyTile):
            top_matches = orientation.top_border == top.bottom_border
        if right and not isinstance(right, EmptyTile):
            right_matches = orientation.right_border == right.left_border
        if bottom and not isinstance(bottom, EmptyTile):
            bottom_matches = orientation.bottom_border == bottom.top_border
        if left and not isinstance(left, EmptyTile):
            left_matches = orientation.left_border == left.right_border
        all_match = top_matches and right_matches and bottom_matches and left_matches
        # if left_matches and not (all_match):
        #     print("something else doesn't match! matched left!")
        # if not all_match:
        #     if not top_matches:
        #         print("top_matches was False!")
# 
#             if not right_matches:
#                 print("right_matches was False!")
# 
#             if not bottom_matches:
#                 print("bottom_matches was False!")
# 
#             if not left_matches:
#                 print("left_matches was False!")

        return all_match
    
    for y in range(edge_length):
        for x in range(edge_length):
            print(f"Looking for position {x},{y}")
            for idx, image in enumerate((imgs := [i for i in images if not i.skip])):
                print(f"Trying image {idx+1}/{len(imgs)}")
                print(image)
                top, right, bottom, left = (None, None, None, None)
                
                if y >= 1:
                    top = image.data[y-1][x]
                    print("setting top")
                if x <= edge_length - 2:
                    right = image.data[y][x+1]
                    print("setting right")
                if y <= edge_length - 2:
                    bottom = image.data[y+1][x]
                    print("setting bottom")
                if x >= 1:
                    left = image.data[y][x-1]
                    print("setting left")
                    #print(f"Setting left to {left}")

                candidates = [o for t in tiles for o in t.calc_orientations() if t.tileId not in map(lambda x: x.tileId, image.tiles()) and fits(o, top, right, bottom, left)]
                print(candidates)
                # if (x, y) == (0, 0):
                #     print("Special case: top left corner")
                #     candidates = [o for o in top_left_candidates if o.tileId not in map(lambda x: x.tileId, image.tiles()) and fits(o, top, right, bottom, left)]
                #     print(candidates)
                # elif (x, y) == (0, edge_length-1):
                #     candidates = [o for o in top_right_candidates if o.tileId not in map(lambda x: x.tileId, image.tiles()) and fits(o, top, right, bottom, left)]
                # elif (x, y) == (edge_length-1, 0):
                #     candidates = [o for o in bottom_left_candidates if o.tileId not in map(lambda x: x.tileId, image.tiles()) and fits(o, top, right, bottom, left)]
                # elif (x, y) == (edge_length-1, edge_length-1):
                #     candidates = [o for o in bottom_right_candidates if o.tileId not in map(lambda x: x.tileId, image.tiles()) and fits(o, top, right, bottom, left)]
                # 
                print(f"choosing from {len(candidates)} candidates for pos {x}")
                finished = False
                if len(candidates) < 1:
                    print(f"Can't go on, deleting idx {idx}")
                    image.skip = True
                    continue
                elif len(candidates) == 1:
                    image.data[y][x] = candidates[0]
                    if (x,y) == (edge_length - 1, edge_length - 1):
                        print(image)
                        finished = True
                elif len(candidates) > 1:
                    #print("####################")
                    #for c in candidates:
                    #    print(c)
                    #    print(c.flipped_horizontal)
                    #    print(c.flipped_vertical)
                    #print("####################")
                    c = candidates[0]
                    image.data[y][x] = c
                    #print(f"1: {c}")
                    #print(image)
                    for c in candidates[1:]:
                        #print(f"n: {c}")
                        ni = image.deepcopy()
                        ni.data[y][x] = c
                        if (x,y) == (edge_length - 1, edge_length - 1):
                            print(ni)
                            finished = True
                            break
                        #print(ni)
                        print(f"Branching new possibility at pos {x}")
                        images.append(ni)
                        #return
                images = [i for i in images if not i.skip]
                if finished:
                    return

    print(images)
    
#    i = 0
#    for x in range(edge_length):
#        for y in range(edge_length):
#            for tile in tiles:
#                for orientation in tile.calc_orientations():
#                    i+=1
#                    #print(i)
    return 0

def part2b(text):
    blocks = text.split("\n\n")
    edge_length = (len(blocks[0].split("\n")[1])+10)//11
    
    noborders = ""
    for y, block in enumerate(blocks):
        for z, row in enumerate(block.split("\n")):
            if z <= 1 or z > 9:
                continue
            for x in range(0, edge_length):
                i = x*11
                line_segment = row[i+1:i+9]
                #noborders += row + "\n" #debug
                noborders += line_segment
                #noborders += " " #debug
                #print(line_segment, end='')
            #if z < edge_length-1:
            noborders += "\n"
        #noborders += "\n" #debug
    noborders = noborders[:-1]

    # print("########################################################")
    # print(noborders)
    # print("########################################################")
    # return
    
    def search_for_sea_monsters(flipped, rotation, text):
        if flipped:
            text = "\n".join(map(lambda l: "".join(l), map(reversed, text.split("\n"))))
        for i in range(rotation):
            data = text.split("\n")
            res = []
            for column in range(len(data[0])):
                s = ""
                for row in reversed(data):
                    #print(f"data = {data}")
                    #print(f"column = {column}")
                    #print(f"row = {row}")
                    s += row[column]
                res.append(s)
            #print(f"s = {s}")
            text = "\n".join(res)
            #print(text)

        #print(text)
        pixels_per_side = len(text.split("\n")[0])

        # sea monster
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
                #print(f"looking for monsters at: x:{x},y:{y}")
                #print(top)
                #print(middle)
                #print(bottom)
                if sea_monster_top.fullmatch(top) and sea_monster_middle.fullmatch(middle) and sea_monster_bottom.fullmatch(bottom):
                    print(f"Found seamonster at x:{x},y:{y} <----------------------------------------------------------------")
                    sea_monster_count += 1
        if sea_monster_count:
            water_roughness -= 15 * sea_monster_count
        return sea_monster_count, water_roughness
        
        
    for fh in [False, True]:
        for rotation in range(4):
            c, r = search_for_sea_monsters(fh, rotation, noborders)
            #print(f"Finished looking for seamonster in this orientation: flipped:{fh},rotation:{rotation}")
            if c > 0:
                return r
#    for y, row in enumerate(data):
#        for x, tile in enumerate(row):
#            for i in range(edge_length):
#            
#                print(tile[1:-1], end='ö')
#        print("hlhlh")
            

# Tile 1951  Tile 2311  Tile 3079 
# #...##.#.. ..###..### #.#.#####.
# ..#.#..#.# ###...#.#. .#..######
# .###....#. ..#....#.. ..#.......
# ###.##.##. .#.#.#..## ######....
# .###.##### ##...#.### ####.#..#.
# .##.#....# ##.##.###. .#...#.##.
# #...###### ####.#...# #.#####.##
# .....#..## #...##..#. ..#.###...
# #.####...# ##..#..... ..#.......
# #.##...##. ..##.#..#. ..#.###...

            
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
#assert_equals(part1(sample1), 20899048083289)
#assert_equals(part2(sample1), 20899048083289)
sample1solved = """Tile 1951  Tile 2311  Tile 3079 
#...##.#.. ..###..### #.#.#####.
..#.#..#.# ###...#.#. .#..######
.###....#. ..#....#.. ..#.......
###.##.##. .#.#.#..## ######....
.###.##### ##...#.### ####.#..#.
.##.#....# ##.##.###. .#...#.##.
#...###### ####.#...# #.#####.##
.....#..## #...##..#. ..#.###...
#.####...# ##..#..... ..#.......
#.##...##. ..##.#..#. ..#.###...

Tile 2729  Tile 1427  Tile 2473 
#.##...##. ..##.#..#. ..#.###...
##..#.##.. ..#..###.# ##.##....#
##.####... .#.####.#. ..#.###..#
####.#.#.. ...#.##### ###.#..###
.#.####... ...##..##. .######.##
.##..##.#. ....#...## #.#.#.#...
....#..#.# #.#.#.##.# #.###.###.
..#.#..... .#.##.#..# #.###.##..
####.#.... .#..#.##.. .######...
...#.#.#.# ###.##.#.. .##...####

Tile 2971  Tile 1489  Tile 1171 
...#.#.#.# ###.##.#.. .##...####
..#.#.###. ..##.##.## #..#.##..#
..####.### ##.#...##. .#.#..#.##
#..#.#..#. ...#.#.#.. .####.###.
.#..####.# #..#.#.#.# ####.###..
.#####..## #####...#. .##....##.
##.##..#.. ..#...#... .####...#.
#.#.###... .##..##... .####.##.#
#...###... ..##...#.. ...#..####
..#.#....# ##.#.#.... ...##....."""
assert_equals(part2b(sample1solved), 273)

#inputtext = read_file_one_string(sys.argv[0].replace("py", "input"))
#print(part1(inputtext))
#print(part2(inputtext))
inputtext = read_file_one_string(sys.argv[0].replace("py", "input.solved"))
print(part2b(inputtext))
