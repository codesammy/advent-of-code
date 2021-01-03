from collections import defaultdict
from dataclasses import dataclass, field
from itertools import permutations
from operator import itemgetter
from pathlib import Path
import re
import sys
from typing import Dict, List
from unittest import TestCase

def part1(text, w, h):
    layers = [x for x in re.split(r'(.{' + str(w*h) + '})', text) if x]
    counts = [(x.count('0'), x.count('1') * x.count('2')) for x in layers]
    zeros, product = min(counts, key=itemgetter(0))
    return product

class Test(TestCase):

    def runTest(self):
        sample = '123456789012'
        self.assertEqual(part1(sample, 3, 2), 1)

if __name__ == '__main__' or True:
    Test().debug()
    inputtext = Path(sys.argv[0].replace("py", "input")).read_text().strip()
    # find the layer that contains the fewest 0 digits
    # On that layer, what is the number of 1 digits multiplied by the number of 2 digits?
    print(part1(inputtext, 25, 6))
