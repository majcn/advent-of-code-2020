from aocd import data as input_data
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
    data.insert(0, 0)
    data.append(data[-1] + 3)

    last_used = {0: 1}
    for i in range(1, len(data) - 1):
        prev_last_used = last_used
        last_used = defaultdict(int)
        for f, v in prev_last_used.items():
            if data[i + 1] - f <= 3:
                last_used[f] += v
            last_used[data[i]] += v

    return next(iter(last_used.values()))


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
