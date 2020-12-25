from aocd import data as input_data
import re


def parse_data():
    result = []
    tmp = {}
    for line in input_data.split('\n'):
        if line == '':
            result.append(tmp)
            tmp = {}
            continue

        entries = line.split(' ')
        for entry in entries:
            k, v = entry.split(':')
            tmp[k] = v

    result.append(tmp)

    return result


def validate_byr(x):
    return 1920 <= int(x) <= 2002


def validate_iyr(x):
    return 2010 <= int(x) <= 2020


def validate_eyr(x):
    return 2020 <= int(x) <= 2030


def validate_hgt(x):
    m = re.match(r'^(\d+)(cm|in)$', x)
    if not m:
        return False

    v, u = m.groups()
    if u == 'cm':
        return 150 <= int(v) <= 193
    else:
        return 59 <= int(v) <= 76


def validate_hcl(x):
    m = re.match(r'^#([0-9]|[a-f]){6}$', x)
    return True if m else False


def validate_ecl(x):
    return x in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']


def validate_pid(x):
    m = re.match(r'^([0-9]){9}$', x)
    return True if m else False


def validate_cid(x):
    return True


def valid_passports(data):
    all_keys = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'}

    result = []
    for d in data:
        if (set(d.keys()) | {'cid'}) == all_keys:
            result.append(d)

    return result


def solve_a(data):
    return len(valid_passports(data))


def solve_b(data):
    passports = valid_passports(data)

    return sum(1 for passport in passports if all(eval(f'validate_{k}("{v}")') for k, v in passport.items()))


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
