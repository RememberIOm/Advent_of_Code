def applicable_rule(stone):
    if stone == 0:
        return (1,)
    elif len(str(stone)) % 2 == 0:
        return (
            int(str(stone)[: len(str(stone)) // 2]),
            int(str(stone)[len(str(stone)) // 2 :]),
        )
    else:
        return (stone * 2024,)


def solution(input_data):
    stones = list(map(int, input_data[0].split()))

    blinks = [stones]

    while len(blinks) <= 25:
        new_stones = []
        prev_stones = blinks[-1]

        for stone in prev_stones:
            new_stones.extend(applicable_rule(stone))

        blinks.append(new_stones)

    return len(blinks[-1])


if __name__ == "__main__":
    INPUT_FILE_PATH = "input.txt"

    with open(INPUT_FILE_PATH, "r") as file:
        data = [line.rstrip() for line in file]

    print(solution(data))
