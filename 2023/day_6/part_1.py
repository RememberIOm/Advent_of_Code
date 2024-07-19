from math import prod


def cal_win(time, distance):
    return sum(
        True if (time - push) * push > distance else False for push in range(time)
    )


def solution(input_data):
    time_list = list(map(int, input_data[0].split(":")[1].split()))
    distance_list = list(map(int, input_data[1].split(":")[1].split()))

    return prod(
        cal_win(time, distance) for time, distance in zip(time_list, distance_list)
    )


input_file = "input.txt"

with open(input_file, "r") as file:
    data = list(map(str.rstrip, file.readlines()))

print(solution(data))
