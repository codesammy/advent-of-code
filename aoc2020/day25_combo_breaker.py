import sys
sys.path.append('../')
from util import read_file, assert_equals

from itertools import count
import math

def handshake(subject_number, loopsize):
    value = 1
    for _ in range(loopsize):
        value *= subject_number
        value = value % 20201227
    return value

def part1(card_public_key, door_public_key):
    value = 1
    for i in count(start=1):
        value = (value * 7) % 20201227
        if value == card_public_key:
            return handshake(door_public_key, i)
        elif value == door_public_key:
            return handshake(card_public_key, i)

card_public_key = 5764801
door_public_key = 17807724
assert_equals(part1(card_public_key, door_public_key), 14897079)

card_public_key = 6930903
door_public_key = 19716708
print(part1(card_public_key, door_public_key))
