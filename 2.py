from aocd import data as input_data
import re


def parse_data():
    result = []
    for x in input_data.split('\n'):
        m = re.match(r'^(\d+)-(\d+) ([a-z]): ([a-z]+)$', x)
        pr = list(m.groups())
        pr[0] = int(pr[0])
        pr[1] = int(pr[1])
        result.append(pr)

    return result


def solve_a(data):
    valid_counter = 0
    for entry in data:
        count = len([1 for x in entry[3] if x == entry[2]])
        valid_counter += entry[0] <= count <= entry[1]
    return valid_counter


def solve_b(data):
    valid_counter = 0
    for entry in data:
        first_c = entry[3][entry[0] - 1]
        second_c = entry[3][entry[1] - 1]

        if first_c == entry[2] and second_c != entry[2]:
            valid_counter += 1

        if first_c != entry[2] and second_c == entry[2]:
            valid_counter += 1

    return valid_counter


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
