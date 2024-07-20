def cal_win(time, distance):
    return sum(
        True if (time - push) * push > distance else False for push in range(time)
    )


def solution(input_data):
    time = int("".join(input_data[0].split(":")[1].split()))
    distance = int("".join(input_data[1].split(":")[1].split()))

    return cal_win(time, distance)


input_file = "input.txt"

with open(input_file, "r") as file:
    data = list(map(str.rstrip, file.readlines()))

print(solution(data))
