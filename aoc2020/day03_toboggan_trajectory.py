import sys
import math
sys.path.append('../')

from util import read_file, assert_equals

def replace_pos(string, position, character):
    result = ""
    i = 0
    for i, c in enumerate(string):
        if i != position:
            result += c
        else:
            result += character
    if position == 31:
        print(string)
        print(position)
        print(result)
    return result

def part1(forest, right, down):
    pos_x = 0
    pos_y = 0
    tree_count = 0
    while True:
        pos_x = pos_x + right
        pos_y = pos_y + down
        if pos_y > len(forest) - 1:
            break
        x_idx = pos_x % (len(forest[0]))
        if forest[pos_y][x_idx] == "#":
            forest[pos_y] = replace_pos(forest[pos_y], x_idx, "X")
            tree_count += 1
        else:
            forest[pos_y] = replace_pos(forest[pos_y], x_idx, "O")
    for i in forest:
        print(i.strip())
    return tree_count

def part2(forest):
    slopes = [(1,1),(3,1),(5,1),(7,1),(1,2)]
    return math.prod(map(lambda s: part1(forest.copy(), s[0], s[1]), slopes))

sample = [
"..##.......",
"#...#...#..",
".#....#..#.",
"..#.#...#.#",
".#...##..#.",
"..#.##.....",
".#.#.#....#",
".#........#",
"#.##...#...",
"#...##....#",
".#..#...#.#"]
assert_equals(part1(sample, 1, 1), 2)
assert_equals(part1(sample, 3, 1), 7)
assert_equals(part1(sample, 5, 1), 3)
assert_equals(part1(sample, 7, 1), 4)
assert_equals(part1(sample, 1, 2), 2)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines, 3, 1))
lines = read_file(sys.argv[0].replace("py", "input"))
print(part2(lines))

