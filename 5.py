from aocd import data as input_data


def parse_data():
    return [x for x in input_data.split('\n')]


def get_position(code):
    rl = 0
    rh = 127

    for x in code[:7]:
        d = (rh - rl) / 2
        d = int(d) if d < 0.5 else int(d) + 1
        if x == 'F':
            rh -= d
        else:
            rl += d

    cl = 0
    ch = 7
    for x in code[7:]:
        d = (ch - cl) / 2
        d = int(d) if d < 0.5 else int(d) + 1
        if x == 'L':
            ch -= d
        else:
            cl += d

    return rh, ch


def get_id(position):
    return position[0] * 8 + position[1]


def solve_a(data):
    return max(get_id(get_position(code)) for code in data)


def solve_b(data):
    positions = {get_position(code) for code in data}
    for x in range(128):
        for y in range(8):
            if (x, y) not in positions \
                    and (x + 1, y) in positions \
                    and (x, y + 1) in positions \
                    and (x - 1, y) in positions \
                    and (x, y - 1) in positions:
                return get_id((x, y))


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
