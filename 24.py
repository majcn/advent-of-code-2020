from aocd import data as input_data
from enum import Enum


class Color(Enum):
    WHITE = 0
    BLACK = 1


class MyDefaultDict(dict):
    def __init__(self):
        super().__init__()

        self.default_value = Color.WHITE

    def __getitem__(self, item):
        if item in self:
            return super().__getitem__(item)

        return self.default_value


def parse_data():
    result = []
    for line in input_data.split('\n'):
        tmp = []
        i = 0
        while i < len(line):
            if line[i] in ['s', 'n']:
                tmp.append(line[i] + line[i + 1])
                i += 2
            else:
                tmp.append(line[i])
                i += 1
        result.append(tmp)
    return result


def solve_part_a(data):
    result = MyDefaultDict()

    for line in data:
        x, y = 0, 0
        for d in line:
            if d == 'nw':
                x = x - 1
                y = y + 1
            elif d == 'ne':
                x = x + 1
                y = y + 1
            elif d == 'e':
                x = x + 2
            elif d == 'se':
                x = x + 1
                y = y - 1
            elif d == 'sw':
                x = x - 1
                y = y - 1
            elif d == 'w':
                x = x - 2

        result[x, y] = Color.WHITE if result[x, y] == Color.BLACK else Color.BLACK

    return result


def adjacent(x, y):
    return (x - 1, y + 1), (x + 1, y + 1), (x + 2, y), (x + 1, y - 1), (x - 1, y - 1), (x - 2, y)


def solve_a(data):
    result = solve_part_a(data)
    return sum(1 for r in result if result[r] == Color.BLACK)


def solve_b(data):
    result = solve_part_a(data)

    for i in range(100):
        for x, y in list(result):
            for a in adjacent(x, y):
                result[a] = result[a]  # => result[a] if a in result else result.default_value

        new_result = MyDefaultDict()
        for x, y in result:
            n_a_b = sum(1 for a in adjacent(x, y) if result[a] == Color.BLACK)
            if result[x, y] == Color.WHITE and n_a_b == 2:
                new_result[x, y] = Color.BLACK
            elif result[x, y] == Color.BLACK and (n_a_b == 1 or n_a_b == 2):
                new_result[x, y] = Color.BLACK

        result = new_result

    return sum(1 for r in result if result[r] == Color.BLACK)


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
