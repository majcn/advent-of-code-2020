from aocd import data as input_data


def parse_data():
    result = {}
    for y, dy in enumerate(input_data.split('\n')):
        for x, dx in enumerate(dy):
            if dx == '#':
                result[(x, y)] = 1
            else:
                result[(x, y)] = 0

    return result


def find_trees(data, dx, dy):
    max_x = max(data.keys(), key=lambda k: k[0])[0] + 1
    max_y = max(data.keys(), key=lambda k: k[1])[1] + 1

    result = 0

    x = 0
    y = 0
    while y < max_y:
        result += data[(x, y)]
        x = (x + dx) % max_x
        y += dy

    return result


def solve_a(data):
    return find_trees(data, 3, 1)


def solve_b(data):
    moves = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]

    result = 1
    for move in moves:
        result *= find_trees(data, move[0], move[1])

    return result


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
