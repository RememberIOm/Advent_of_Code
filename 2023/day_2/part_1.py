def cal_num(input_game):
    game_idx = int(input_game.split(": ")[0].split()[1])
    game_list = input_game.split(": ")[1].split("; ")

    for game_element in game_list:
        game_element_list = game_element.split(", ")

        game_element_dict = {}

        for element in game_element_list:
            element = element.split()
            game_element_dict[element[1]] = int(element[0])

        if not (
            game_element_dict.get("red", 0) <= 12
            and game_element_dict.get("green", 0) <= 13
            and game_element_dict.get("blue", 0) <= 14
        ):
            return 0

    return game_idx


input_file = "input.txt"

with open(input_file, "r") as file:
    data = list(map(str.rstrip, file.readlines()))

print(sum(cal_num(i) for i in data))
