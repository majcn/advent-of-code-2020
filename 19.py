from aocd import data as input_data


def parse_data():
    rules = {}
    codes = []

    found_empty_line = False
    for x in input_data.split('\n'):
        if not x:
            found_empty_line = True
            continue

        if not found_empty_line:
            left, right = x.split(': ')
            rules[left] = [tuple(el.split(' ')) for el in right.replace('"', '').split(' | ')]
        else:
            codes.append(x)

    return rules, codes


def checker(text, key, rules):
    result = []
    for rule in rules[key]:
        partial_result = ['']

        if rule[0] in ['a', 'b']:
            partial_result = [r + rule[0] for r in partial_result if text.startswith(r + rule[0])]
        else:
            for rule_part in rule:
                tmp = []
                for r1 in partial_result:
                    c_text = text[len(r1):]
                    tmp += [r1 + r2 for r2 in checker(c_text, rule_part, rules) if text.startswith(r1 + r2)]
                    partial_result = tmp

        result += partial_result
    return result


def solve(rules, codes):
    return sum(1 for c in codes if any(c == cc for cc in checker(c, '0', rules)))


def solve_a(data):
    rules, codes = data

    return solve(rules, codes)


def solve_b(data):
    rules, codes = data

    rules['8'] = [('42',), ('42', '8')]
    rules['11'] = [('42', '31'), ('42', '11', '31')]

    return solve(rules, codes)


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
