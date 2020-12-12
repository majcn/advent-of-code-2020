from aocd import data as input_data
from enum import Enum


class Direction(Enum):
    NORTH = 'N'
    EAST = 'E'
    SOUTH = 'S'
    WEST = 'W'


def parse_data():
    return [(x[0], int(x[1:])) for x in input_data.split('\n')]


def next_direction_a(direction, dir_code, value):
    value = value % 360
    if dir_code == 'L':
        value = 360 - value

    switcher = {
        Direction.NORTH: Direction.EAST,
        Direction.EAST:  Direction.SOUTH,
        Direction.SOUTH: Direction.WEST,
        Direction.WEST:  Direction.NORTH,
    }

    n = direction
    while value > 0:
        n = switcher[n]
        value = value - 90

    return n


def next_position_a(position, direction, value):
    switcher = {
        Direction.NORTH: lambda x, y: (x, y + value),
        Direction.EAST:  lambda x, y: (x + value, y),
        Direction.SOUTH: lambda x, y: (x, y - value),
        Direction.WEST:  lambda x, y: (x - value, y),
    }

    return switcher[direction](*position)


def next_waypoint_rotate_b(waypoint, dir_code, value):
    value = value % 360
    if dir_code == 'L':
        value = 360 - value

    n = waypoint
    while value > 0:
        x, y = n
        n = (y, -x)
        value = value - 90

    return n


def next_waypoint_move_b(waypoint, dir_code, value):
    switcher = {
        Direction.NORTH: lambda x, y: (x, y + value),
        Direction.EAST:  lambda x, y: (x + value, y),
        Direction.SOUTH: lambda x, y: (x, y - value),
        Direction.WEST:  lambda x, y: (x - value, y),
    }

    return switcher[Direction(dir_code)](*waypoint)


def next_position_b(position, waypoint, value):
    px, py = position
    wx, wy = waypoint
    return px + wx * value, py + wy * value


def solve_a(data):
    direction = Direction.EAST
    position = (0, 0)
    for c, v in data:
        if c in ['R', 'L']:
            direction = next_direction_a(direction, c, v)
        elif c == 'F':
            position = next_position_a(position, direction, v)
        else:
            position = next_position_a(position, Direction(c), v)

    return sum(map(abs, position))


def solve_b(data):
    waypoint = (10, 1)
    position = (0, 0)
    for c, v in data:
        if c in ['R', 'L']:
            waypoint = next_waypoint_rotate_b(waypoint, c, v)
        elif c == 'F':
            position = next_position_b(position, waypoint, v)
        else:
            waypoint = next_waypoint_move_b(waypoint, c, v)

    return sum(map(abs, position))


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
