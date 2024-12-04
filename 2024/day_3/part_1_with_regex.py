import re


def solution(input_data):
    # Join the input data into a single string
    input_data = "".join(input_data)

    # Find all "mul()" substrings
    mul_occurrences = re.findall(r"mul\((\d+),(\d+)\)", input_data)

    return sum(int(a) * int(b) for a, b in mul_occurrences)


INPUT_FILE_PATH = "input.txt"

with open(INPUT_FILE_PATH, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
