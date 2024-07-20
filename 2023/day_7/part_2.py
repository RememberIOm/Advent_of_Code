from functools import cmp_to_key
from itertools import chain


def card_power(card):
    card_dict = {}

    for card_char in card:
        if card_char in card_dict:
            card_dict[card_char] += 1
        else:
            card_dict[card_char] = 1

    card_dict_values = list(sorted(card_dict.values()))
    j_num = card_dict.get("J", 0)

    if j_num:
        card_dict_values.remove(j_num)

        if card_dict_values:
            card_dict_values[-1] += j_num
        else:
            card_dict_values.append(j_num)

    card_dict_values = tuple(card_dict_values)

    card_power_dict = {
        (5,): 6,  # 5 of a kind
        (1, 4): 5,  # 4 of a kind
        (2, 3): 4,  # Full house
        (1, 1, 3): 3,  # 3 of a kind
        (1, 2, 2): 2,  # 2 pairs
        (1, 1, 1, 2): 1,  # 1 pair
        (1, 1, 1, 1, 1): 0,  # High card
    }

    return card_power_dict[card_dict_values]


def high_card_comp(a, b):
    high_card_dict = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
        "J": 1,
    }

    for a_elem, b_elem in zip(a[0], b[0]):
        if a_elem == b_elem:
            continue

        a_elem = high_card_dict[a_elem]
        b_elem = high_card_dict[b_elem]

        return a_elem - b_elem


def solution(input_data):
    cards = tuple((card, int(bid)) for card, bid in map(str.split, input_data))

    CARD_POWER_NUM = 7
    card_power_list = tuple([] for _ in range(CARD_POWER_NUM))

    for card, bid in cards:
        card_power_list[card_power(card)].append((card, bid))

    card_power_list = chain.from_iterable(
        sorted(card_power, key=cmp_to_key(high_card_comp))
        for card_power in card_power_list
    )

    return sum(rank * bid for rank, (_, bid) in enumerate(card_power_list, start=1))


input_file = "input.txt"

with open(input_file, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
