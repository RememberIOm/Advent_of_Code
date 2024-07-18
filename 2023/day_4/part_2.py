def match_card(card):
    winning_num, my_num = card

    winning_num_set = set(winning_num)
    my_num_set = set(my_num)

    return len(winning_num_set & my_num_set)


def duplicate_card(matched_score):
    matched_score_len = len(matched_score)

    card_num_list = [1] * matched_score_len

    for i in range(matched_score_len):
        card_num = card_num_list[i]

        for j in range(1, matched_score[i] + 1):
            card_num_list[i + j] += card_num

    return sum(card_num_list)


def cal_num(input_card):
    card = [i.split(": ")[1].split(" | ") for i in input_card]
    card = [[list(map(int, j.split())) for j in i] for i in card]

    matched_score = [match_card(card_i) for card_i in card]

    return duplicate_card(matched_score)


input_file = "input.txt"

with open(input_file, "r") as file:
    data = list(map(str.rstrip, file.readlines()))

print(cal_num(data))
