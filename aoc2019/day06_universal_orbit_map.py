from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
import re
import sys
from typing import Dict, List
from unittest import TestCase

def parse_input(text):
    graph = defaultdict(set)
    invgraph = defaultdict(set)
    orbit_pattern = re.compile(r'(\w+)\)(\w+)')
    for line in text.split('\n'):
        center, orbit = orbit_pattern.fullmatch(line).groups()
        graph[orbit].add(center)
        invgraph[center].add(orbit)
    return graph, invgraph

def part1(text):
    graph, _ = parse_input(text)
    def count_orbits(node, n=0):
        count = 0
        while (node := list(graph[node])[0]) != 'COM':
            count += 1
        return count + 1
    return sum(count_orbits(n) for n in graph.keys())

def part2(text):
    graph, invgraph = parse_input(text)
    def orbits(node, n=0):
        nodes = list()
        while (node := list(graph[node])[0]) != 'COM':
            nodes.append(node)
        return nodes
    you_orbits = orbits('YOU')
    san_orbits = orbits('SAN')
    intersections = set(you_orbits).intersection(set(san_orbits))
    return min(you_orbits.index(x) + san_orbits.index(x) for x in intersections)

class Test(TestCase):

    def runTest(self):

#         G - H       J - K - L
#        /           /
# COM - B - C - D - E - F
#                \
#                 I
        sample1 = """COM)B
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
        self.assertEqual(part1(sample1), 42)

#                           YOU
#                          /
#         G - H       J - K - L
#        /           /
# COM - B - C - D - E - F
#                \
#                 I - SAN
        sample2 = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""
        self.assertEqual(part2(sample2), 4)

if __name__ == '__main__' or True:
    Test().debug()
    inputtext = Path(sys.argv[0].replace("py", "input")).read_text()
    # What is the total number of direct and indirect orbits in your map data?
    print(part1(inputtext))
    print(part2(inputtext))
