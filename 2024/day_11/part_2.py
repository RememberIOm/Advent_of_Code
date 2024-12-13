from functools import cache


THRESHOLD = 75


@cache
def applicable_rule(stone, depth=0):
    if depth == THRESHOLD:
        return 1

    if stone == 0:
        result = applicable_rule(1, depth + 1)
    elif len(str(stone)) % 2 == 0:
        result = applicable_rule(
            int(str(stone)[: len(str(stone)) // 2]), depth + 1
        ) + applicable_rule(int(str(stone)[len(str(stone)) // 2 :]), depth + 1)
    else:
        result = applicable_rule(stone * 2024, depth + 1)

    return result


def solution(input_data):
    stones = list(map(int, input_data[0].split()))

    return sum(applicable_rule(stone) for stone in stones)


if __name__ == "__main__":
    INPUT_FILE_PATH = "input.txt"

    with open(INPUT_FILE_PATH, "r") as file:
        data = [line.rstrip() for line in file]

    print(solution(data))
