from aocd import data as input_data
import re


def parse_data():
    types = {}
    for x in input_data.split('\n'):
        if not x:
            break
        t, rule_1_from, rule_1_to, rule_2_from, rule_2_to = re.match(r'(.*): (\d+)-(\d+) or (\d+)-(\d+)', x).groups()
        types[t] = (int(rule_1_from), int(rule_1_to), int(rule_2_from), int(rule_2_to))

    my_ticket_line = next(i for i, x in enumerate(input_data.split('\n')) if x == "your ticket:") + 1
    my_ticket = [int(xx) for xx in input_data.split('\n')[my_ticket_line].split(',')]

    nearby_tickets = []
    found_nearby_tickets = False
    for x in input_data.split('\n'):
        if found_nearby_tickets:
            nearby_tickets.append([int(xx) for xx in x.split(',')])

        if x == 'nearby tickets:':
            found_nearby_tickets = True

    return types, my_ticket, nearby_tickets


def apply_rule(x, rule):
    return rule[0] <= x <= rule[1] or rule[2] <= x <= rule[3]


def get_invalid_fields(ticket, rules):
    result = []
    for t in ticket:
        if not any(apply_rule(t, rule) for rule in rules):
            result.append(t)

    return result


def solve_a(data):
    types, my_ticket, nearby_tickets = data

    return sum(sum(get_invalid_fields(t, types.values())) for t in nearby_tickets)


def solve_b(data):
    types, my_ticket, nearby_tickets = data

    valid_tickets = [t for t in nearby_tickets if not get_invalid_fields(t, types.values())]

    valid_types_for_column = []
    for i in range(len(valid_tickets[0])):
        valid_type_names = set()
        for type_name, rule in types.items():
            if all(apply_rule(nearby_ticket[i], rule) for nearby_ticket in valid_tickets):
                valid_type_names.add(type_name)

        valid_types_for_column.append(valid_type_names)

    all_options = set(types.keys())
    fields = {}
    while all_options:
        for column, valid_types in enumerate(valid_types_for_column):
            if len(valid_types) == 1:
                v = valid_types.pop()
                fields[column] = v
                all_options.remove(v)

        valid_types_for_column = [x & all_options for x in valid_types_for_column]

    result = 1
    for i, name in fields.items():
        if name.startswith('departure'):
            result *= my_ticket[i]

    return result


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
