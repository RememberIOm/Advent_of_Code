def match_card(card):
    winning_num, my_num = card

    winning_num_set = set(winning_num)
    my_num_set = set(my_num)

    return int(2 ** (len(winning_num_set & my_num_set) - 1))


def cal_num(input_card):
    card = [i.split(": ")[1].split(" | ") for i in input_card]
    card = [[list(map(int, j.split())) for j in i] for i in card]

    return sum(match_card(card_i) for card_i in card)


input_file = "input.txt"

with open(input_file, "r") as file:
    data = list(map(str.rstrip, file.readlines()))

print(cal_num(data))
