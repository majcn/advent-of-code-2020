from aocd import data as input_data
import re


def parse_data():
    result = {}
    for x in input_data.split('\n'):
        key, value_str = re.match(r'^(.*) bags contain (.*)$', x).groups()
        value = {}
        for xx in value_str.split(', '):
            m = re.match('^([0-9]+) (.*) (bag|bags)\\.?$', xx)
            if m:
                value[m.group(2)] = m.group(1)
        result[key] = value
    return result


def f_a(data, key):
    return key == 'shiny gold' or any(f_a(data, vk) for vk in data[key])


def f_b(data, key):
    if not data[key]:
        return 1

    return 1 + sum(f_b(data, vk) * int(vv) for vk, vv in data[key].items())


def solve_a(data):
    return sum(f_a(data, x) for x in data) - 1


def solve_b(data):
    return f_b(data, 'shiny gold') - 1


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
