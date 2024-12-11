from collections import deque


def is_loop(input_data):
    directions = "^>v<"
    directions_map = {
        "^": (-1, 0),
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1),
    }

    for i in range(len(input_data)):
        for j in range(len(input_data[i])):
            if input_data[i][j] in directions:
                x, y = i, j
                direction = input_data[i][j]
                break

    visited_positions = {(x, y)}
    direction_change_count = 0
    THRESHOLD = 1000

    while 0 <= x < len(input_data) and 0 <= y < len(input_data[x]):
        if input_data[x][y] != "#":
            visited_positions.add((x, y))

            x += directions_map[direction][0]
            y += directions_map[direction][1]
        else:
            x -= directions_map[direction][0]
            y -= directions_map[direction][1]

            direction = directions[(directions.index(direction) + 1) % 4]
            direction_change_count += 1

            x += directions_map[direction][0]
            y += directions_map[direction][1]

            if direction_change_count == THRESHOLD:
                return True

    return False


def solution(input_data):
    input_data = list(input_data)

    loop_num = 0

    for i in range(len(input_data)):
        for j in range(len(input_data[i])):
            if input_data[i][j] == ".":
                input_data[i] = input_data[i][:j] + "#" + input_data[i][j + 1 :]

                loop_num += is_loop(input_data)

                input_data[i] = input_data[i][:j] + "." + input_data[i][j + 1 :]

    return loop_num


INPUT_FILE_PATH = "input.txt"

with open(INPUT_FILE_PATH, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
