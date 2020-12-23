from aocd import data as input_data


def parse_data():
    decks = [[int(line) for line in deck_as_str.split('\n')[1:]] for deck_as_str in input_data.split('\n\n')]

    result = []
    for deck_as_array in decks:
        deck_as_number = 0
        i = 0
        for card_index in range(len(deck_as_array)):
            deck_as_number += deck_as_array[len(deck_as_array) - card_index - 1] * (10 ** i)
            i += 2
        result.append(Deck(deck_as_number, len(deck_as_array)))

    return result


class Deck:
    def __init__(self, deck, deck_size):
        self.deck = deck
        self.deck_size = deck_size

    def draw_a_card(self):
        modifier = (10 ** ((self.deck_size - 1) * 2))
        card = self.deck // modifier
        self.deck = self.deck % modifier
        self.deck_size = self.deck_size - 1
        return card

    def put_on_bottom(self, card_1, card_2):
        self.deck = self.deck * 100 + card_1
        self.deck = self.deck * 100 + card_2
        self.deck_size += 2

    def score(self):
        result = 0
        tmp_deck = self.deck
        for i in range(self.deck_size):
            x = tmp_deck % 100
            tmp_deck = tmp_deck // 100
            result += x * (i + 1)
        return result

    def size(self):
        return self.deck_size

    def copy(self, size):
        x = self.deck // 10 ** ((self.deck_size - size) * 2)
        return Deck(x, size)


def hash_deck_1_and_deck_2(deck_1, deck_2):
    max_size = deck_1.size() + deck_2.size()
    return deck_1.deck * 10 ** max_size + deck_2.deck


def solve_part_a(deck_1, deck_2):
    while deck_1.size() > 0 and deck_2.size() > 0:
        card_1 = deck_1.draw_a_card()
        card_2 = deck_2.draw_a_card()

        if card_1 > card_2:
            deck_1.put_on_bottom(card_1, card_2)
        else:
            deck_2.put_on_bottom(card_2, card_1)

    return deck_1, deck_2


def solve_part_b(deck_1, deck_2):
    cache = set()
    while deck_1.size() > 0 and deck_2.size() > 0:
        tmp = hash_deck_1_and_deck_2(deck_1, deck_2)
        if tmp in cache:
            return Deck(None, 1), Deck(None, 0)
        cache.add(tmp)

        card_1 = deck_1.draw_a_card()
        card_2 = deck_2.draw_a_card()

        if card_1 <= deck_1.size() and card_2 <= deck_2.size():
            r_1, r_2 = solve_part_b(deck_1.copy(card_1), deck_2.copy(card_2))
            if r_1.size() > 0:
                deck_1.put_on_bottom(card_1, card_2)
            else:
                deck_2.put_on_bottom(card_2, card_1)
        else:
            if card_1 > card_2:
                deck_1.put_on_bottom(card_1, card_2)
            else:
                deck_2.put_on_bottom(card_2, card_1)

    return deck_1, deck_2


def solve(deck_1, deck_2, solve_part_x):
    r_1, r_2 = solve_part_x(deck_1, deck_2)

    return r_1.score() if r_1.size() > 0 else r_2.score()


def solve_a(data):
    deck_1, deck_2 = data
    return solve(deck_1, deck_2, solve_part_a)


def solve_b(data):
    deck_1, deck_2 = data
    return solve(deck_1, deck_2, solve_part_b)


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
