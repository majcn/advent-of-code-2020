from aocd import data as input_data


class Node:
    def __init__(self, label):
        self.next_node = None
        self.label = label


def parse_data():
    nodes = {}

    x = int(input_data[0])
    first_node = Node(x)
    nodes[x] = first_node

    generate_nodes(nodes, first_node, map(int, input_data[1:]))

    return nodes, first_node


def generate_nodes(nodes, first_node, array_of_data):
    node = first_node
    for x in array_of_data:
        tmp = Node(x)
        nodes[x] = tmp

        node.next_node = tmp
        node = tmp

    node.next_node = first_node


def solve(nodes, first_node, min_label, max_label, nr_i):
    current_cup = first_node
    for i in range(nr_i):
        picked_cup_1 = current_cup.next_node
        picked_cup_2 = picked_cup_1.next_node
        picked_cup_3 = picked_cup_2.next_node

        current_cup.next_node = picked_cup_3.next_node

        destination_cup_label = current_cup.label
        while True:
            destination_cup_label -= 1
            if destination_cup_label < min_label:
                destination_cup_label = max_label

            if destination_cup_label not in [picked_cup_1.label, picked_cup_2.label, picked_cup_3.label]:
                break

        destination_cup = nodes[destination_cup_label]
        picked_cup_3.next_node = destination_cup.next_node
        destination_cup.next_node = picked_cup_1

        current_cup = current_cup.next_node

    return nodes[1]


def solve_a(data):
    nodes, first_node = data
    min_label, max_label, nr_i = 1, 9, 100

    node_1 = solve(nodes, first_node, min_label, max_label, nr_i)

    result = ""
    node = node_1.next_node
    while node != node_1:
        result += str(node.label)
        node = node.next_node
    return result


def solve_b(data):
    nodes, first_node = data
    min_label, max_label, nr_i = 1, 1000000, 10000000

    last_node = next(x for x in nodes.values() if x.next_node == first_node)
    generate_nodes(nodes, last_node, range(max(nodes) + 1, max_label + 1))
    nodes[max_label].next_node = first_node

    node_1 = solve(nodes, first_node, min_label, max_label, nr_i)

    return node_1.next_node.label * node_1.next_node.next_node.label


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
