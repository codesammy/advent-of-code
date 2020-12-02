import sys
import re
sys.path.append('../')

from util import read_file, assert_equals
line_pattern = re.compile('([0-9]+)-([0-9]+) (.): (.*)')

def extract(line):
    return line_pattern.match(line).groups()

def part1(lines):
    valid_count = 0
    for l in lines:
        minimum, maximum, char, text = extract(l)
        char_occurences = text.count(char)
        if char_occurences <= int(maximum) and char_occurences >= int(minimum):
            valid_count += 1
    return valid_count

def part2(lines):
    valid_count = 0
    for l in lines:
        pos1, pos2, char, text = extract(l)
        p1 = text[int(pos1)-1] == char
        p2 = text[int(pos2)-1] == char
        if (p1 == True and p2 == False) or (p1 == False and p2 == True):
            valid_count += 1
    return valid_count

sample = ["1-3 a: abcde",
         "1-3 b: cdefg",
         "2-9 c: ccccccccc"]
assert_equals(part1(sample), 2)
assert_equals(part2(sample), 1)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines))
print(part2(lines))
