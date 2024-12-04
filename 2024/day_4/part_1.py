import re


def count_overlapping_occurrences(string, substring):
    return len(re.findall(f"(?={substring})", string))


def get_diagonals(input_data):
    add_front_padding = (
        " " * i + line + " " * (len(line) - i - 1) for i, line in enumerate(input_data)
    )
    add_back_padding = (
        " " * (len(line) - i - 1) + line + " " * i for i, line in enumerate(input_data)
    )

    down_diagonals = tuple(map(str.strip, map("".join, zip(*add_front_padding))))
    up_diagonals = tuple(map(str.strip, map("".join, zip(*add_back_padding))))

    return down_diagonals, up_diagonals


def solution(input_data):
    # Serialize the input data
    horizontals = input_data
    verticals = tuple(map("".join, zip(*input_data)))
    down_diagonals, up_diagonals = get_diagonals(input_data)

    checked_strings = (
        horizontals,
        verticals,
        down_diagonals,
        up_diagonals,
    )

    # Count the number of "XMAS" occurrences
    result = 0

    # Check each string
    for strings in checked_strings:
        # Check each substring
        for string in strings:
            result += count_overlapping_occurrences(string, "XMAS")
            result += count_overlapping_occurrences(string[::-1], "XMAS")

    return result


INPUT_FILE_PATH = "input.txt"

with open(INPUT_FILE_PATH, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
