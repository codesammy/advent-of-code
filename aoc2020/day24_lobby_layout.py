import sys
sys.path.append('../')
from util import read_file, assert_equals

from dataclasses import dataclass, field
from typing import Dict, List
from itertools import cycle, islice
from collections import defaultdict
import math
import re

def parse_input(lines):
    direction_pattern = re.compile(r'nw|ne|sw|se|e|w')
    for line in lines:
        yield direction_pattern.findall(line)

def part1(text):
    flipped = defaultdict(bool)
    tile_paths = list(parse_input(text))
    direction_to_offset = {
        'nw':(-1, 1),
        'ne':( 1, 1),
        'sw':(-1,-1),
        'se':( 1,-1),
        'e' :( 2, 0),
        'w' :(-2, 0)
    }
    for path in tile_paths:
        x, y = (0, 0)
        for direction in path:
            xo, yo = direction_to_offset[direction]
            x += xo
            y += yo
        flipped[(x, y)] = not flipped[(x, y)]
    return sum(1 for v in flipped.values() if v)

sample = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew""".split("\n")
assert_equals(part1(sample), 10)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines))
