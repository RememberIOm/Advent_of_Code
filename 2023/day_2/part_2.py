import math


def cal_num(input_game):
    game_idx = int(input_game.split(": ")[0].split()[1])
    game_list = input_game.split(": ")[1].split("; ")

    game_element_dict = {"red": 0, "blue": 0, "green": 0}

    for game_element in game_list:
        game_element_list = game_element.split(", ")

        for element in game_element_list:
            element = element.split()
            game_element_dict[element[1]] = max(
                game_element_dict[element[1]], int(element[0])
            )

    return math.prod(game_element_dict.values())


input_file = "input.txt"

with open(input_file, "r") as file:
    data = list(map(str.rstrip, file.readlines()))

print(sum(cal_num(i) for i in data))
