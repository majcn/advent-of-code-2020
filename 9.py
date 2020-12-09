from aocd import data as input_data
from itertools import combinations


def parse_data():
    return [int(x) for x in input_data.split('\n')]


def solve_a(data):
    preamble_len = 25
    for i in range(len(data) - preamble_len):
        part = data[i:i+preamble_len]
        next_number = data[i + preamble_len]
        if not any(n1 + n2 == next_number for n1, n2 in combinations(part, 2)):
            return next_number


def solve_b(data):
    invalid_number = solve_a(data)
    for n in range(2, len(data)):
        for i in range(len(data) - n):
            part = data[i:i+n]
            if sum(part) == invalid_number:
                return min(part) + max(part)


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
