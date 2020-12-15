from aocd import data as input_data


def parse_data():
    my_timestamp = int(input_data.split('\n')[0])
    bus_ids = {i: int(x) for i, x in enumerate(input_data.split('\n')[1].split(',')) if x != 'x'}
    return my_timestamp, bus_ids


def chinese_remainder(n, a):
    result = 0
    prod = 1
    for x in n:
        prod *= x
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        result += a_i * mul_inv(p, n_i) * p
    return result % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def solve_a(data):
    my_timestamp, bus_ids = data
    min_bus_id = bus_ids[0]
    min_waiting_time = 100000000000
    for bus_id in bus_ids.values():
        waiting_time = bus_id - (my_timestamp % bus_id)
        if waiting_time < min_waiting_time:
            min_waiting_time = waiting_time
            min_bus_id = bus_id

    return min_bus_id * min_waiting_time


def solve_b(data):
    my_timestamp, bus_ids = data

    n = []
    a = []
    for diff, bus_id in bus_ids.items():
        n.append(bus_id)
        a.append(-diff)

    return chinese_remainder(n, a)


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
