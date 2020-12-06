from aocd import data as input_data


def parse_data():
    return [list(map(set, x.split('\n'))) for x in input_data.split('\n\n')]


def solve_a(data):
    return sum(len(set.union(*x)) for x in data)


def solve_b(data):
    return sum(len(set.intersection(*x)) for x in data)


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
