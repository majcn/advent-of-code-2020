from aocd import data as input_data


def parse_data():
    return [int(x) for x in input_data.split(',')]


def solve(data, nr_iterations):
    value = {data[i]: i for i in range(len(data) - 1)}
    last_element = data[-1]
    prev_last_element = data[-2]

    for N in range(len(data) - 1, nr_iterations):
        prev_last_element = last_element
        last_element = N - value[last_element] if last_element in value else 0
        value[prev_last_element] = N

    return prev_last_element


def solve_a(data):
    return solve(data, 2020)


def solve_b(data):
    return solve(data, 30000000)


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
