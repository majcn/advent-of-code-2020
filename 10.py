from aocd import data as input_data
from itertools import combinations
from collections import defaultdict


def parse_data():
    return sorted([int(x) for x in input_data.split('\n')])


def solve_a(data):
    differences = defaultdict(int)
    prev = 0
    for x in data:
        differences[x - prev] += 1
        prev = x
    return differences[1] * (differences[3] + 1)


def solve_b(data):
    last = data[-1]
    data.insert(0, 0)
    data.append(data[-1] + 3)
    data.append(data[-1] + 3)
    data.append(data[-1] + 3)

    i = 1
    last_used = {0: 1}
    while True:
        prev_last_used = last_used
        last_used = defaultdict(int)
        for f, v in prev_last_used.items():
            for c in range(3):
                for x in combinations(data[i:i+3], c + 1):
                    to_validate = (f,) + x + (data[i + 3], data[i + 4])
                    if all(to_validate[i + 1] - to_validate[i] <= 3 for i in range(len(to_validate) - 1)):
                        last_used[x[-1]] += v

        if len(last_used.keys()) == 1 and list(last_used.keys())[0] > last:
            return list(last_used.values())[0]

        i += 3


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
