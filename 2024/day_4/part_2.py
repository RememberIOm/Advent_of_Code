def is_xmas(block):
    center_char = block[1][1]
    angle_chars = block[0][0] + block[0][2] + block[2][0] + block[2][2]

    valid_angle_chars = {"MMSS", "SSMM", "MSMS", "SMSM"}

    return center_char == "A" and angle_chars in valid_angle_chars


def solution(input_data):
    result = 0

    for i in range(1, len(input_data) - 1):
        for j in range(1, len(input_data[i]) - 1):
            block = (
                input_data[i - 1][j - 1 : j + 2],
                input_data[i][j - 1 : j + 2],
                input_data[i + 1][j - 1 : j + 2],
            )

            result += is_xmas(block)

    return result


INPUT_FILE_PATH = "input.txt"

with open(INPUT_FILE_PATH, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
