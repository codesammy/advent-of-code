from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
import re
import sys
from typing import Dict, List
from unittest import TestCase

def parse_input(text):
    graph = defaultdict(set)
    orbit_pattern = re.compile(r'(\w+)\)(\w+)')
    for line in text.split('\n'):
        center, orbit = orbit_pattern.fullmatch(line).groups()
        graph[orbit].add(center)
    return graph

def part1(text):
    graph = parse_input(text)
    def count_orbits(node, n=0):
        count = 0
        while (node := list(graph[node])[0]) != 'COM':
            count += 1
        return count + 1

    return sum(count_orbits(n) for n in graph.keys())

class Test(TestCase):

#         G - H       J - K - L
#        /           /
# COM - B - C - D - E - F
#                \
#                 I

    def runTest(self):
        sample = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""
        self.assertEqual(part1(sample), 42)

if __name__ == '__main__' or True:
    Test().debug()
    inputtext = Path(sys.argv[0].replace("py", "input")).read_text()
    # What is the total number of direct and indirect orbits in your map data?
    print(part1(inputtext))
