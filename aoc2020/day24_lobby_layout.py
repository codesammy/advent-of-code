import sys
sys.path.append('../')
from util import read_file, assert_equals

from collections import defaultdict
import re

direction_to_offset = {
    'nw':(-1, 1),
    'ne':( 1, 1),
    'sw':(-1,-1),
    'se':( 1,-1),
    'e' :( 2, 0),
    'w' :(-2, 0)
}

def flip_tiles(tile_paths):
    flipped = defaultdict(bool)
    for path in tile_paths:
        x, y = (0, 0)
        for direction in path:
            xo, yo = direction_to_offset[direction]
            x += xo
            y += yo
        flipped[(x, y)] = not flipped[(x, y)]
    return flipped

def parse_input(lines):
    direction_pattern = re.compile(r'nw|ne|sw|se|e|w')
    for line in lines:
        yield direction_pattern.findall(line)

def part1(text):
    tile_paths = list(parse_input(text))
    flipped = flip_tiles(tile_paths)
    return sum(1 for v in flipped.values() if v)

def part2(text):
    tile_paths = list(parse_input(text))
    flipped = flip_tiles(tile_paths)

    def neighbors(x, y):
        return [(x+xo, y+yo) for xo, yo in direction_to_offset.values()]

    # make sure all neighbors exist
    for k, v in flipped.copy().items():
        for x, y in neighbors(*k):
            flipped[(x, y)]

    for day in range(100):
        new_state = dict()
        for coords, old_state in flipped.copy().items():
            black_neighbor_count = 0
            for x, y in neighbors(*coords):
                black_neighbor_count += flipped[(x, y)]
            # Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
            if old_state and (black_neighbor_count == 0 or black_neighbor_count > 2):
                new_state[coords] = False
            # Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
            elif not old_state and black_neighbor_count == 2:
                new_state[coords] = True
        flipped.update(new_state)
        print(f"Day {day+1}: {sum(1 for v in flipped.values() if v)}")
    
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
assert_equals(part2(sample), 2208)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines))
print(part2(lines))
