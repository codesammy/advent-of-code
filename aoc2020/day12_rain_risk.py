import sys
from itertools import starmap
from functools import reduce
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

    def __repr__(self):
        return f"CardinalPoint.{self.name}"

class RotationDirection(Enum):
    LEFT = -1
    RIGHT = 1

class MoveDirection(Enum):
    FORWARD = 1
    
class InstructionFactory:
    def __init__(self, move_instruction_class):
        self.move_instruction_class = move_instruction_class
        
    def create(self, kind, amount):
        if isinstance(kind, CardinalPoint):
            return self.move_instruction_class(kind, amount)
        elif isinstance(kind, RotationDirection):
            return TurnInstruction(kind, amount)
        elif isinstance(kind, MoveDirection):
            return ForwardMoveInstruction(amount)
        else:
            raise NotImplementedError

class MoveInstruction():
    def __init__(self, cardinalPoint, amount):
        self.cardinalPoint = cardinalPoint
        self.amount = amount

    def execute(self, waypoint, pos):
        move_vector = tuple(map(self.amount.__mul__, self.cardinalPoint.value))
        new_pos = tuple(starmap(add, zip(move_vector, pos)))
        return (waypoint, new_pos)

class WaypointMoveInstruction():
    def __init__(self, cardinalPoint, amount):
        self.cardinalPoint = cardinalPoint
        self.amount = amount

    def execute(self, waypoint, pos):
        move_vector = tuple(map(self.amount.__mul__, self.cardinalPoint.value))
        new_pos = tuple(starmap(add, zip(move_vector, waypoint.vector())))
        new_waypoint = Waypoint.of(new_pos)
        return (new_waypoint, pos)
    
class ForwardMoveInstruction():
    def __init__(self, amount):
        self.amount = amount

    def execute(self, waypoint, pos):
        move_vector = tuple(map(self.amount.__mul__, waypoint.vector()))
        new_pos = tuple(starmap(add, zip(move_vector, pos)))
        return (waypoint, new_pos)

class TurnInstruction():
    def __init__(self, rotationDirection, amount):
        self.rotationDirection = rotationDirection
        self.amount = amount

    def execute(self, waypoint, pos):
        new_waypoint = Waypoint([Course(self.turn_course(c.orientation), c.amount) for c in waypoint.courses])
        return (new_waypoint, pos)

    def turn_course(self, cardinalPoint):
        cardinal_points = list(CardinalPoint) * 2
        i = cardinal_points.index(cardinalPoint)
        new_orientation = cardinal_points[i + self.rotationDirection.value * int(self.amount / 90)]
        return new_orientation

class Ferry:
    def __init__(self, waypoint):
        self.pos = (0, 0)
        self.waypoint = waypoint

    def sail(self, instructions):
        for instruction in instructions:
            self.waypoint, self.pos = instruction.execute(self.waypoint, self.pos)

class Course:
    def __init__(self, orientation, amount):
        self.orientation = orientation
        self.amount = amount

    def scalar(self):
        return self.orientation.value * self.amount

    def vector(self):
        return tuple(map(self.amount.__mul__, self.orientation.value))

    def __repr__(self):
        return f"Course({repr(self.orientation)}, {self.amount})"

class Waypoint:
    def __init__(self, courses):
        self.courses = courses

    def vector(self):
        return reduce(lambda v, e: (v[0] + e[0], v[1] + e[1]), map(Course.vector, self.courses))

    def __repr__(self):
        return f"Waypoint({repr(self.courses)})"

    @classmethod
    def of(cls, vector):
        courses = []
        if vector[0] != 0:
            unit_ew = int(vector[0] / abs(vector[0]))
            ew = [None, CardinalPoint.EAST, CardinalPoint.WEST][unit_ew]
            courses.append(Course(ew, abs(vector[0])))
        if vector[1] != 0:
            unit_ns = int(vector[1] / abs(vector[1]))
            ns = [None, CardinalPoint.NORTH, CardinalPoint.SOUTH][unit_ns]
            courses.append(Course(ns, abs(vector[1])))
        return Waypoint(courses)

def parse_instructions(rows, move_instruction_class):
    instruction_pattern = re.compile(r'(.)(\d+)')
    instruction_factory = InstructionFactory(move_instruction_class)
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
        yield instruction_factory.create(instruction, amount)

def part1(rows):
    course = parse_instructions(rows, MoveInstruction)
    ferry = Ferry(Waypoint([Course(CardinalPoint.EAST, 1)]))
    ferry.sail(course)
    return add(*map(abs, ferry.pos))

def part2(rows):
    course = parse_instructions(rows, WaypointMoveInstruction)
    ferry = Ferry(Waypoint([Course(CardinalPoint.EAST, 10), Course(CardinalPoint.NORTH, 1)]))
    ferry.sail(course)
    return add(*map(abs, ferry.pos))

sample1 = """F10
N3
F7
R90
F11""".split("\n")
assert_equals(part1(sample1), 25)
assert_equals(part2(sample1), 286)

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines))
print(part2(lines))
