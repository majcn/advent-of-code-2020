from aocd import data as input_data
from itertools import permutations
from collections import defaultdict

TILE_SIZE = len(input_data.split('\n')[1])
IMAGE_SIZE = int(len(input_data.split('Tile')) ** 0.5)


def parse_data():
    tiles = {}

    tile_id = None
    for i, line in enumerate(input_data.split('\n')):
        c = i % (TILE_SIZE + 2)
        if c == 0:
            tile_id = int(line[5:-1])
            tiles[tile_id] = {}
        elif c <= TILE_SIZE:
            for li, ld in enumerate(line):
                tiles[tile_id][(li, c - 1)] = ld

    return tiles


def get_top(a):
    return [a[0][x] for x in range(TILE_SIZE)]


def get_right(a):
    return [a[y][TILE_SIZE - 1] for y in range(TILE_SIZE)]


def get_bottom(a):
    return [a[TILE_SIZE - 1][x] for x in range(TILE_SIZE)]


def get_left(a):
    return [a[y][0] for y in range(TILE_SIZE)]


def get_all_rotations_and_flips(a):
    result = []

    rotated = a
    for i in range(4):
        rotated = [list(r) for r in zip(*rotated[::-1])]
        result.append(rotated)

    a_flip = [line[::-1] for line in a]
    rotated = a_flip
    for i in range(4):
        rotated = [list(r) for r in zip(*rotated[::-1])]
        result.append(rotated)

    return result


def get_options(tile):
    options = []

    tile_as_2d_array = [[tile[(x, y)] for x in range(TILE_SIZE)] for y in range(TILE_SIZE)]

    for a in get_all_rotations_and_flips(tile_as_2d_array):
        top = get_top(a)
        right = get_right(a)
        bottom = get_bottom(a)
        left = get_left(a)

        option = (a, top, right, bottom, left)
        options.append(option)

    return options


def get_rotated_0_0_tile(result, tiles, first_tile_id):
    right_tile_id, bottom_tile_id = result[first_tile_id]

    first_tile_options = get_options(tiles[first_tile_id])
    right_tile_options = get_options(tiles[right_tile_id])
    bottom_tile_options = get_options(tiles[bottom_tile_id])

    for o1 in first_tile_options:
        for o2 in right_tile_options:
            for o3 in bottom_tile_options:
                tile_1_array, _, right_1, bottom_1, _ = o1
                _, _, _, _, left_2 = o2
                _, top_3, _, _, _ = o3

                if right_1 == left_2 and bottom_1 == top_3:
                    return tile_1_array, first_tile_id


def find_match_next_to_left(image, x, y, tiles, matches):
    prev_array, _ = image[(x - 1, y)]
    right_of_prev_array = get_right(prev_array)

    for m in matches:
        for mo in get_options(tiles[m]):
            mo_array, _, _, _, left = mo
            if right_of_prev_array == left:
                return mo_array, m


def find_match_next_to_top(image, x, y, tiles, matches):
    prev_array, _ = image[(x, y - 1)]
    bottom_of_prev_array = get_bottom(prev_array)

    for m in matches:
        for mo in get_options(tiles[m]):
            mo_array, top, _, _, _ = mo
            if bottom_of_prev_array == top:
                return mo_array, m


def find_match_next_to_left_and_top(image, x, y, tiles, matches):
    left_array, _ = image[(x - 1, y)]
    right_of_left_array = get_right(left_array)

    top_array, _ = image[(x, y - 1)]
    bottom_of_top_array = get_bottom(top_array)

    for m in matches:
        for mo in get_options(tiles[m]):
            mo_array, top, _, _, left = mo
            if bottom_of_top_array == top and right_of_left_array == left:
                return mo_array, m


def image_to_2d_array(image):
    r = []
    for y in range(IMAGE_SIZE):
        for ty in range(1, TILE_SIZE - 1):
            tmp = []
            for x in range(IMAGE_SIZE):
                for tx in range(1, TILE_SIZE - 1):
                    tmp.append(image[(x, y)][0][ty][tx])
            r.append(tmp)
    return r


def get_image(tiles):
    result = defaultdict(set)
    for tile_id_1, tile_id_2 in permutations(tiles.keys(), 2):
        tile_1_options = get_options(tiles[tile_id_1])
        tile_2_options = get_options(tiles[tile_id_2])

        for o1 in tile_1_options:
            for o2 in tile_2_options:
                _, top_1, right_1, bottom_1, left_1 = o1
                _, top_2, right_2, bottom_2, left_2 = o2

                if top_1 == bottom_2 or right_1 == left_2 or bottom_1 == top_2 or left_1 == right_2:
                    result[tile_id_1].add(tile_id_2)

    match_2 = set(key for key, value in result.items() if len(value) == 2)
    match_3 = set(key for key, value in result.items() if len(value) == 3)
    match_4 = set(key for key, value in result.items() if len(value) == 4)

    image = {}
    max_x = IMAGE_SIZE - 1
    max_y = IMAGE_SIZE - 1

    image[(0, 0)] = get_rotated_0_0_tile(result, tiles, match_2.pop())

    y = 0
    for x in range(1, IMAGE_SIZE - 1):
        el = find_match_next_to_left(image, x, y, tiles, match_3)
        image[(x, y)] = el
        match_3.remove(el[1])
    el = find_match_next_to_left(image, max_x, 0, tiles, match_2)
    image[(max_x, 0)] = el
    match_2.remove(el[1])

    x = 0
    for y in range(1, IMAGE_SIZE - 1):
        el = find_match_next_to_top(image, x, y, tiles, match_3)
        image[(x, y)] = el
        match_3.remove(el[1])
    el = find_match_next_to_top(image, 0, max_y, tiles, match_2)
    image[(0, max_y)] = el
    match_2.remove(el[1])

    y = max_y
    for x in range(1, IMAGE_SIZE - 1):
        el = find_match_next_to_left(image, x, y, tiles, match_3)
        image[(x, y)] = el
        match_3.remove(el[1])
    el = find_match_next_to_left(image, max_x, max_y, tiles, match_2)
    image[(max_x, max_y)] = el
    match_2.remove(el[1])

    x = max_x
    for y in range(1, IMAGE_SIZE - 1):
        el = find_match_next_to_top(image, x, y, tiles, match_3)
        image[(x, y)] = el
        match_3.remove(el[1])

    for y in range(1, IMAGE_SIZE - 1):
        for x in range(1, IMAGE_SIZE - 1):
            el = find_match_next_to_left_and_top(image, x, y, tiles, match_4)
            image[(x, y)] = el
            match_4.remove(el[1])

    return image


def solve_a(data):
    image = get_image(data)

    result = 1
    for x, y in [(0, 0), (IMAGE_SIZE - 1, 0), (0, IMAGE_SIZE - 1), (IMAGE_SIZE - 1, IMAGE_SIZE - 1)]:
        result *= image[(x, y)][1]
    return result


def get_sea_monsters(image_as_2d_array):
    sea_monster = [
        (18, 0),
        (0, 1), (5, 1), (6, 1), (11, 1), (12, 1), (17, 1), (18, 1), (19, 1),
        (1, 2), (4, 2), (7, 2), (10, 2), (13, 2), (16, 2)
    ]

    sea_monster_max_x = max(sea_monster, key=lambda el: el[0])[0]
    sea_monster_max_y = max(sea_monster, key=lambda el: el[1])[1]

    number_of_sea_monsters = 0
    for a in get_all_rotations_and_flips(image_as_2d_array):
        for y in range(len(a) - sea_monster_max_y):
            for x in range(len(a) - sea_monster_max_x):
                if all(a[sea_monster_y + y][sea_monster_x + x] == '#' for sea_monster_x, sea_monster_y in sea_monster):
                    number_of_sea_monsters += 1

    return number_of_sea_monsters, len(sea_monster)


def solve_b(data):
    image = get_image(data)
    image_as_2d_array = image_to_2d_array(image)

    nr_sea_monsters, size_of_sea_monster = get_sea_monsters(image_as_2d_array)

    return len([el for line in image_as_2d_array for el in line if el == "#"]) - nr_sea_monsters * size_of_sea_monster


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
