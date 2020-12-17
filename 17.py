from aocd import data as input_data


def parse_data():
    result = set()
    for y, line in enumerate(input_data.split('\n')):
        for x, el in enumerate(line):
            if el == '#':
                result.add((x, y, 0, 0))
    return result


def find_inactive_neighbors(data, el, dimensions):
    result = set()
    el_x, el_y, el_z, el_w = el

    dw_range = [0] if dimensions == 3 else [-1, 0, 1]
    for dw in dw_range:
        for dz in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    d_el = (el_x + dx, el_y + dy, el_z + dz, el_w + dw)
                    if el != d_el and d_el not in data:
                        result.add(d_el)
    return result


def solve(data, dimensions):
    max_neighbors = (3 ** dimensions) - 1

    active_queue = data
    for i in range(6):
        inactive_queue = set()
        new_active_queue = set()
        for el in active_queue:
            inactive_neighbors = find_inactive_neighbors(active_queue, el, dimensions)
            if (max_neighbors - len(inactive_neighbors)) in [2, 3]:
                new_active_queue.add(el)
            inactive_queue.update(inactive_neighbors)

        for el in inactive_queue:
            inactive_neighbors = find_inactive_neighbors(active_queue, el, dimensions)
            if (max_neighbors - len(inactive_neighbors)) == 3:
                new_active_queue.add(el)

        active_queue = new_active_queue

    return len(active_queue)


def solve_a(data):
    return solve(data, 3)


def solve_b(data):
    return solve(data, 4)


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
