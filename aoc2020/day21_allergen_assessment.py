import sys
import re
import math
sys.path.append('../')
from util import read_file, assert_equals
from collections import defaultdict
from functools import reduce
from dataclasses import dataclass, field
from typing import Set

@dataclass(frozen=True)
class Food:
    name: str
    ingredients: Set[str] = field(compare=False)
    allergens: Set[str] = field(compare=False)

@dataclass(frozen=True, order=True)
class Allergen:
    name: str
    ingredient: str = field(compare=False)

def parse_input(lines):
    food_pattern = re.compile(r"(\w+(?: \w+)*)+ \(contains (\w+(?:, \w+)*)\)")
    for line in lines:
        ingredients, allergens = food_pattern.fullmatch(line).groups()
        yield Food(ingredients, set(ingredients.split(" ")), set(allergens.split(", ")))

def find_allergens(lines):
    foods = list(parse_input(lines))

    # sort by allergen
    food_by_allergen = defaultdict(set)
    for food in foods:
        for allergen in food.allergens:
            food_by_allergen[allergen].add(food)

    # find intersections between foods for specific allergens
    allergen_ingredient_candidates = defaultdict(set)
    for allergen, foods_containing in food_by_allergen.items():
        allergen_ingredient_candidates[allergen] = reduce(set.intersection, map(lambda f: f.ingredients, foods_containing))

    # find obvious allergens
    allergens = set()
    modified = True
    while modified:
        modified = False
        for allergen, ingredients in allergen_ingredient_candidates.items():
            if len(ingredients) == 1:
                ingredient = list(ingredients)[0]
                allergens.add(Allergen(allergen, ingredient))
                modified = True
                for other_ingredients in allergen_ingredient_candidates.values():
                    if ingredient in other_ingredients:
                        other_ingredients.discard(ingredient)
    return allergens, foods

def part1(lines):
    allergens, foods = find_allergens(lines)

    # count non allergens
    return sum(len(food.ingredients.difference({a.ingredient for a in allergens})) for food in foods)

def part2(lines):
    allergens, _ = find_allergens(lines)
    return ",".join(map(lambda a: a.ingredient, sorted(allergens)))

sample1 = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)""".split("\n")
assert_equals(part1(sample1), 5)
assert_equals(part2(sample1), "mxmxvkd,sqjhc,fvjkl")

lines = read_file(sys.argv[0].replace("py", "input"))
print(part1(lines))
print(part2(lines))
