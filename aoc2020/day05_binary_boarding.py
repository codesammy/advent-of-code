import sys
import re
sys.path.append('../')
from util import read_file, assert_equals

class BoardingPass:
    binary_space_partition_pattern = re.compile("(.{7})(.{3})")

    def from_seat_position(self, row, column):
        self.row, self.column = row, column
        self.seat_id = self.row * 8 + self.column
        return self

    def from_binary_space_partition(self, binary_space_partition):
        self.binary_space_partition = binary_space_partition
        self.from_seat_position(*self.convert_binary_space_partition(self.binary_space_partition))
        return self

    def convert_binary_space_partition(self, binary_space_partition):
        row_code, column_code = self.binary_space_partition_pattern.match(binary_space_partition).groups()
        row = int(row_code.translate(str.maketrans("FB", "01")), 2)
        column = int(column_code.translate(str.maketrans("LR", "01")), 2)
        return (row, column)

    def __str__(self):
        return "BoardingPass[%s, %s, %s, %s]" % (self.binary_space_partition, self.row, self.column, self.seat_id)

def part1(lines):
    return max(BoardingPass().from_binary_space_partition(l).seat_id for l in lines)

def part2(lines):
    taken_seats = [BoardingPass().from_binary_space_partition(l).seat_id for l in lines]
    leftover_seats = set(range(min(taken_seats), max(taken_seats) + 1)) - set(taken_seats)
    return leftover_seats.pop()

assert_equals(part1(["FBFBBFFRLR"]), 357)
assert_equals(part1(["BFFFBBFRRR"]), 567)
assert_equals(part1(["FFFBBBFRRR"]), 119)
assert_equals(part1(["BBFFBBFRLL"]), 820)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines))
print(part2(lines))
