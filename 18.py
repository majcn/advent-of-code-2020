from aocd import data as input_data


def parse_data():
    return [x.replace(' ', '') for x in input_data.split('\n')]


def find_number(eq, start):
    i = start
    while i < len(eq):
        x = eq[i]
        if x.isnumeric():
            i += 1
        else:
            break

    return int(eq[start:i]), i - start - 1


def solve_simple_a(numbers, operators):
    result = numbers[0]
    for i in range(len(operators)):
        result = eval(f'{result} {operators[i]} {numbers[i + 1]}')
    return result


def solve_simple_b(numbers, operators):
    i = 0
    while i < len(operators):
        operator = operators[i]
        if operator == '+':
            operators.pop(i)
            right = numbers.pop(i + 1)
            left = numbers.pop(i)
            numbers.insert(i, left + right)
        else:
            i += 1

    return solve_simple_a(numbers, operators)


def solver(eq, start, solve_simple):
    i = start

    operators = []
    numbers = []
    while i < len(eq):
        x = eq[i]

        if x == '(':
            n, skip_i = solver(eq, i + 1, solve_simple)
            numbers.append(n)
            i += skip_i
        elif x == ')':
            return solve_simple(numbers, operators), i - start + 1
        elif x in ['+', '*']:
            operators.append(x)
        else:
            n, skip_i = find_number(eq, i)
            numbers.append(n)
            i += skip_i

        i += 1

    return solve_simple(numbers, operators)


def solve_a(data):
    return sum(solver(x, 0, solve_simple_a) for x in data)


def solve_b(data):
    return sum(solver(x, 0, solve_simple_b) for x in data)


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
