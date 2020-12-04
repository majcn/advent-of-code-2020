from aocd import data as input_data
from itertools import combinations


def parse_data():
    return [int(x) for x in input_data.split('\n')]


def solve_a(data):
    return next(x * y for x, y in combinations(data, 2) if x + y == 2020)


def solve_b(data):
    return next(x * y * z for x, y, z in combinations(data, 3) if x + y + z == 2020)


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
