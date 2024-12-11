def solution(input_data):
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

    while 0 <= x < len(input_data) and 0 <= y < len(input_data[x]):
        if input_data[x][y] != "#":
            visited_positions.add((x, y))

            x += directions_map[direction][0]
            y += directions_map[direction][1]
        else:
            x -= directions_map[direction][0]
            y -= directions_map[direction][1]

            direction = directions[(directions.index(direction) + 1) % 4]

            x += directions_map[direction][0]
            y += directions_map[direction][1]

    return len(visited_positions)


INPUT_FILE_PATH = "input.txt"

with open(INPUT_FILE_PATH, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
