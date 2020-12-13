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

def part2(_, bus_ids):
    bus_ids_with_offset = [(int(b), i) for i,b in enumerate(bus_ids) if b != 'x']
    step = 1
    timestamp = 1
    for bus_id, offset in bus_ids_with_offset:
        while (timestamp + offset) % bus_id != 0:
            timestamp += step
        step *= bus_id
    return timestamp

sample1 = """939
7,13,x,x,59,x,31,19""".split("\n")
assert_equals(part1(*parse_input(sample1)), 295)
assert_equals(part2(*parse_input(sample1)), 1068781)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(*parse_input(lines)))
print(part2(*parse_input(lines)))

# quick hack
# bus_ids_with_offset = [(19, 0), (41, 9), (17, 2), (13, 11), (853, 50), (23, 4)]
# ts = 0
# i = 0
# while True:
#     #print(f"Trying {ts}")
#     if all((ts+o)%b==0 for b,o in bus_ids_with_offset):
#         print(ts)
#         break
#     else:
#         ts = 561179 * i - 19
#         i += 1
