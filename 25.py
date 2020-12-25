from aocd import data as input_data


def parse_data():
    return [int(x) for x in input_data.split('\n')]


def calculate_next_val(val, subject_number):
    return (val * subject_number) % 20201227


def find_loop_size(goal):
    subject_number = 7

    val = 1
    loop_size = 1
    while val != goal:
        val = calculate_next_val(val, subject_number)
        loop_size += 1

    return loop_size - 1


def solve_a(data):
    card_public_key, door_public_key = data

    loop_size = find_loop_size(card_public_key)
    val = 1
    for _ in range(loop_size):
        val = calculate_next_val(val, door_public_key)

    return val


print("Part 1: {}".format(solve_a(parse_data())))
