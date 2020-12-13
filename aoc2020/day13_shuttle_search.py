import sys
from operator import itemgetter
import math
sys.path.append('../')
from util import read_file, assert_equals

def parse_input(lines):
    return int(lines[0]), lines[1].split(',')

def part1(earliest_timestamp, bus_ids):
    def next_departure(bus_id):
        return bus_id, math.ceil(earliest_timestamp / bus_id) * bus_id
    earliest_bus, earliest_bus_timestamp = min((next_departure(int(b)) for b in bus_ids if b != "x"), key=itemgetter(1))
    wait_minutes = abs(earliest_timestamp - earliest_bus_timestamp)
    return earliest_bus * wait_minutes

sample1 = """939
7,13,x,x,59,x,31,19""".split("\n")
assert_equals(part1(*parse_input(sample1)), 295)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(*parse_input(lines)))
