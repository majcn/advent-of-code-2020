from aocd import data as input_data
from enum import Enum


MAX_Y = len(input_data.split('\n'))
MAX_X = len(input_data.split('\n')[0])


class State(Enum):
    FLOOR = 0
    EMPTY_SEAT = 1
    OCCUPIED_SEAT = 2


class MyDefaultDict(dict):
    def __init__(self):
        super().__init__()

        self.default_value = State.FLOOR

    def __getitem__(self, item):
        if item in self:
            return super().__getitem__(item)

        return self.default_value


def parse_data():
    result = MyDefaultDict()
    for y, dy in enumerate(input_data.split('\n')):
        for x, dx in enumerate(dy):
            if dx == 'L':
                result[(x, y)] = State.EMPTY_SEAT
    return result


def find_neighbours_occupied(data, x, y):
    neighbours = (x-1, y), (x-1, y+1), (x, y+1), (x+1, y+1), (x+1, y), (x+1, y-1), (x, y-1), (x-1, y-1)
    return sum(1 for n in neighbours if data[n] == State.OCCUPIED_SEAT)


def find_neighbours_occupied_inf(data, x, y):
    result = 0

    ds = [
        lambda xx, yy: (xx - 1, yy),
        lambda xx, yy: (xx - 1, yy + 1),
        lambda xx, yy: (xx, yy + 1),
        lambda xx, yy: (xx + 1, yy + 1),
        lambda xx, yy: (xx + 1, yy),
        lambda xx, yy: (xx + 1, yy - 1),
        lambda xx, yy: (xx, yy - 1),
        lambda xx, yy: (xx - 1, yy - 1)
    ]

    for d in ds:
        nx, ny = d(x, y)
        while data[(nx, ny)] != State.EMPTY_SEAT and 0 <= nx <= MAX_X and 0 <= ny <= MAX_Y:
            if data[(nx, ny)] == State.OCCUPIED_SEAT:
                result += 1
                break

            nx, ny = d(nx, ny)

    return result


def apply_rules_a(data, x, y):
    if data[(x, y)] == State.EMPTY_SEAT and find_neighbours_occupied(data, x, y) == 0:
        return State.OCCUPIED_SEAT

    if data[(x, y)] == State.OCCUPIED_SEAT and find_neighbours_occupied(data, x, y) >= 4:
        return State.EMPTY_SEAT

    return data[(x, y)]


def apply_rules_b(data, x, y):
    if data[(x, y)] == State.EMPTY_SEAT and find_neighbours_occupied_inf(data, x, y) == 0:
        return State.OCCUPIED_SEAT

    if data[(x, y)] == State.OCCUPIED_SEAT and find_neighbours_occupied_inf(data, x, y) >= 5:
        return State.EMPTY_SEAT

    return data[(x, y)]


def transform(data, apply_rules):
    new_data = MyDefaultDict()
    for x, y in data.keys():
        new_data[(x, y)] = apply_rules(data, x, y)

    return new_data


def count_occupied(data):
    return sum(1 for v in data.values() if v == State.OCCUPIED_SEAT)


def solve(data, apply_rules):
    old_data = transform(data, apply_rules)
    new_data = transform(old_data, apply_rules)

    while old_data != new_data:
        old_data = new_data
        new_data = transform(old_data, apply_rules)

    return count_occupied(new_data)


def solve_a(data):
    return solve(data, apply_rules_a)


def solve_b(data):
    return solve(data, apply_rules_b)


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
