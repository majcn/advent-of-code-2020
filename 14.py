from aocd import data as input_data


def parse_data():
    return [x.split(' = ') for x in input_data.split('\n')]


def solve_a(data):
    mask = {}
    mem = {}
    for code, value in data:
        if code == 'mask':
            mask = {len(value) - x - 1: int(value[x]) for x in range(len(value)) if value[x] != 'X'}
        else:
            mem_loc = int(code[4:-1])
            value = int(value)
            for mk, mv in mask.items():
                if mv == 0:
                    value = value & ~(1 << mk)
                else:
                    value = value | (1 << mk)
            mem[mem_loc] = value

    return sum(mem.values())


def get_all_memory_locations(prev, now):
    result = []
    found_x = False
    for i in range(len(now)):
        if now[i] == 'X':
            result += get_all_memory_locations(prev + now[:i] + '0', now[(i+1):])
            result += get_all_memory_locations(prev + now[:i] + '1', now[(i+1):])
            found_x = True
            break
    if not found_x:
        result.append(prev + now)
    return result


def solve_b(data):
    masks_str = ''
    mem = {}
    for code, value in data:
        if code == 'mask':
            masks_str = value
        else:
            mem_loc = int(code[4:-1])
            value = int(value)

            bin_mem_loc = bin(mem_loc)[2:].zfill(len(masks_str))
            mask = ''
            for i in range(len(masks_str)):
                if masks_str[i] == '0':
                    mask += bin_mem_loc[i]
                else:
                    mask += masks_str[i]

            for memory_location in get_all_memory_locations('', mask):
                mem[int(memory_location, 2)] = value

    return sum(mem.values())


print('Part 1: {}'.format(solve_a(parse_data())))
print('Part 2: {}'.format(solve_b(parse_data())))
