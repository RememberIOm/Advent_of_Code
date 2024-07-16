import re


def cal_num(string):
    num_list = [i if i.isdigit() else "0" for i in string]

    num_str_list = (
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    )

    for i, num_str in enumerate(num_str_list):
        string_find_list = re.finditer(num_str, string)

        for string_find in string_find_list:
            num_list[string_find.start()] = str(i + 1)

    num_list = [i for i in num_list if i != "0"]

    return int(num_list[0] + num_list[-1])


input_file = "temp.txt"

with open(input_file, "r") as file:
    data = list(map(str.rstrip, file.readlines()))

print(sum(cal_num(i) for i in data))
