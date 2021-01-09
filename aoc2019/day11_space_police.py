from collections import defaultdict
from dataclasses import dataclass, field
from itertools import permutations
import math
from operator import itemgetter
from pathlib import Path
import re
import sys
import traceback
from typing import Dict, List
from unittest import TestCase
sys.path.append('.')
from day09_sensor_boost import IntCode3
from day02_1202_program_alarm import OpCode, parse_input

def part1(text):
    state = parse_input(text)
    # 0 black
    # 1 white
    hull = defaultdict(lambda: 0)
    painted_panels = set()
    try:
        robot = IntCode3(state, iter([]))
        # start at 0, 0 facing up
        robot.orientation = (0, -1)
        robot.pos = (0, 0)
        # repeat
        while True:
            color_at_pos = hull[robot.pos]
            robot.add_input(color_at_pos)
            # run until output
            robot.run(4)
            paint_color = robot.get_output()
            hull[robot.pos] = paint_color
            painted_panels.add(robot.pos)
            robot.run(4)
            # 0 left
            # 1 right
            turn_where = robot.get_output()
            if turn_where == 0:
                robot.orientation = (robot.orientation[1], -robot.orientation[0])
            else:
                robot.orientation = (-robot.orientation[1], robot.orientation[0])
            # move forward
            robot.pos = (robot.pos[0] + robot.orientation[0], robot.pos[1] + robot.orientation[1])
    except StopIteration as e:
        return len(painted_panels)

if __name__ == '__main__':
    inputtext = Path(sys.argv[0].replace("py", "input")).read_text().strip()
    # How many panels does it paint at least once?
    print(part1(inputtext))
