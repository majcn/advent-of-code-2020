from aocd import data as input_data
from itertools import permutations


def parse_data():
    rules = []
    all_allergens = set()
    for line in input_data.split('\n'):
        left, right = line[:-1].split(' (contains ')
        ingredients = set(left.split(' '))
        allergens = set(right.split(', '))

        rules.append((ingredients, allergens))
        all_allergens |= allergens

    return rules, all_allergens


def validate(data, rules):
    for ingredients, allergens in rules:
        for allergen in allergens:
            if allergen in data and data[allergen] not in ingredients:
                return False

    return True


def solve_part(rules, init_tmp):
    new_rules = []
    for ingredients, allergens in rules:
        new_ingredients = ingredients - set(init_tmp.values())
        new_allergens = allergens - set(init_tmp.keys())
        new_rules.append((new_ingredients, new_allergens))

    rule_with_max_allergens = max(new_rules, key=lambda r: len(r[1]))

    result = []
    for p in permutations(rule_with_max_allergens[0], len(rule_with_max_allergens[1])):
        tmp = {allergen: ingredient for ingredient, allergen in zip(p, rule_with_max_allergens[1])}

        if validate(tmp, new_rules):
            tmp.update(init_tmp)
            result.append(tmp)

    return result


def solve(rules, all_allergens):
    result = [{}]
    while len(result[0]) < len(all_allergens):
        result = [el for r in result for el in solve_part(rules, r)]

    return result[0]


def solve_a(data):
    rules, all_allergens = data

    my_list = solve(rules, all_allergens)
    return sum(len(ingredients - set(my_list.values())) for ingredients, allergens in rules)


def solve_b(data):
    rules, all_allergens = data

    my_list = solve(rules, all_allergens)
    return ','.join(el[1] for el in sorted(my_list.items(), key=lambda x: x[0]))


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
