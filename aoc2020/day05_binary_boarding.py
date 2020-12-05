import sys
import math
import re
sys.path.append('../')

from util import read_file, assert_equals

class BoardingPass:
    binary_space_partition_pattern = re.compile("(.{7})(.{3})")
    def __init__(self, binary_space_partition):
        self.binary_space_partition = binary_space_partition
        self.row, self.column = self.convert_binary_space_partition(self.binary_space_partition)
        self.seat_id = self.row * 8 + self.column

    def convert_binary_space_partition(self, binary_space_partition):
        row_code, column_code = self.binary_space_partition_pattern.match(binary_space_partition).groups()
            
        row = int(row_code.translate(str.maketrans("FB", "01")), 2)
        column = int(column_code.translate(str.maketrans("LR", "01")), 2)
        return (row, column)

    def __str__(self):
        return "BoardingPass[%s, %s, %s, %s]" % (self.binary_space_partition, self.row, self.column, self.seat_id)

def part1(lines):
    return max(BoardingPass(l).seat_id for l in lines)

assert_equals(BoardingPass("FBFBBFFRLR").seat_id, 357)
assert_equals(BoardingPass("BFFFBBFRRR").seat_id, 567)
assert_equals(BoardingPass("FFFBBBFRRR").seat_id, 119)
assert_equals(BoardingPass("BBFFBBFRLL").seat_id, 820)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines))

