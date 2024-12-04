import re


def solution(input_data):
    # Join the input data into a single string
    input_data = "".join(input_data)

    # Find all "mul()" substrings
    mul_occurrences = re.finditer(r"mul\((\d+),(\d+)\)", input_data)

    result = 0

    for mul_match in mul_occurrences:
        # Check "do()" and "don't()" occurrences
        last_do = input_data.rfind("do()", 0, mul_match.start())
        last_do_not = input_data.rfind("don't()", 0, mul_match.start())

        # If the last "do()" occurrence is after the last "don't()" occurrence
        if last_do >= last_do_not:
            result += int(mul_match.group(1)) * int(mul_match.group(2))

    return result


INPUT_FILE_PATH = "input.txt"

with open(INPUT_FILE_PATH, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
