import sys
from itertools import starmap
from enum import Enum
from operator import add
import re
import math
sys.path.append('../')
from util import read_file, assert_equals

class CardinalPoint(Enum):
    NORTH = (0, 1)
    EAST = (1, 0)
    SOUTH = (0, -1)
    WEST = (-1, 0)

class RotationDirection(Enum):
    LEFT = -1
    RIGHT = 1

class MoveDirection(Enum):
    FORWARD = 1
    
class Instruction:
    @classmethod
    def of(cls, kind, amount):
        if isinstance(kind, CardinalPoint):
            return MoveInstruction(kind, amount)
        elif isinstance(kind, RotationDirection):
            return TurnInstruction(kind, amount)
        elif isinstance(kind, MoveDirection):
            return ForwardMoveInstruction(amount)
        else:
            raise NotImplementedError

class MoveInstruction(Instruction):
    def __init__(self, cardinalPoint, amount):
        self.cardinalPoint = cardinalPoint
        self.amount = amount

    def execute(self, orientation, pos):
        move_vector = tuple(map(self.amount.__mul__, self.cardinalPoint.value))
        new_pos = tuple(starmap(add, zip(move_vector, pos)))
        return (orientation, new_pos)

class ForwardMoveInstruction(Instruction):
    def __init__(self, amount):
        self.amount = amount

    def execute(self, orientation, pos):
        move_vector = tuple(map(self.amount.__mul__, orientation.value))
        new_pos = tuple(starmap(add, zip(move_vector, pos)))
        return (orientation, new_pos)

class TurnInstruction(Instruction):
    def __init__(self, rotationDirection, amount):
        self.rotationDirection = rotationDirection
        self.amount = amount

    def execute(self, orientation, pos):
        cardinal_points = list(CardinalPoint) * 2
        i = cardinal_points.index(orientation)
        new_orientation = cardinal_points[i + self.rotationDirection.value * int(self.amount / 90)]
        return (new_orientation, pos)

class Ferry:
    def __init__(self, orientation):
        self.orientation = orientation
        self.pos = (0, 0)

    def sail(self, instructions):
        for instruction in instructions:
            self.orientation, self.pos = instruction.execute(self.orientation, self.pos)

def parse_instructions(rows):
    instruction_pattern = re.compile(r'(.)(\d+)')
    for row in rows:
        char, number = instruction_pattern.fullmatch(row).groups()
        instruction = {'N':CardinalPoint.NORTH,
                       'S':CardinalPoint.SOUTH,
                       'E':CardinalPoint.EAST,
                       'W':CardinalPoint.WEST,
                       'L':RotationDirection.LEFT,
                       'R':RotationDirection.RIGHT,
                       'F':MoveDirection.FORWARD}[char]
        amount = int(number)
        yield Instruction.of(instruction, amount)

def part1(rows):
    course = parse_instructions(rows)
    ferry = Ferry(CardinalPoint.EAST)
    ferry.sail(course)
    return add(*map(abs, ferry.pos))

sample1 = """F10
N3
F7
R90
F11""".split("\n")
assert_equals(part1(sample1), 25)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines))
