from multiprocessing import Pool
from functools import cache
from tqdm import tqdm
from itertools import chain


@cache
def applicable_rule(stone):
    if stone == 0:
        return (1,)
    elif stone >= 10 and len(str(stone)) % 2 == 0:
        num_digits = len(str(stone))
        half = 10 ** (num_digits // 2)
        return (stone // half, stone % half)
    else:
        return (stone * 2024,)


def solution(input_data):
    stones = list(map(int, input_data[0].split()))

    blink_count = 0
    BLINK_COUNT_THRESHOLD = 75

    progress_stones = stones

    while blink_count < BLINK_COUNT_THRESHOLD:
        with Pool() as pool:
            progress_stones = list(
                chain.from_iterable(tqdm(pool.map(applicable_rule, progress_stones)))
            )

        blink_count += 1

        print(blink_count, len(progress_stones))

    return len(progress_stones)


if __name__ == "__main__":
    INPUT_FILE_PATH = "input.txt"

    with open(INPUT_FILE_PATH, "r") as file:
        data = [line.rstrip() for line in file]

    print(solution(data))
