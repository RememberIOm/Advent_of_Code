def get_bottom(history):
    return tuple(history[i + 1] - history[i] for i in range(len(history) - 1))


def get_bottoms(history):
    bottoms = [history]

    while any(bottoms[-1]):
        bottoms.append(get_bottom(bottoms[-1]))

    return bottoms


def get_prev_history(history):
    bottoms = get_bottoms(history)

    return sum(
        history[0] if idx % 2 == 0 else -history[0]
        for idx, history in enumerate(bottoms)
    )


def solution(input_data):
    histories = tuple(
        map(lambda history: tuple(map(int, history)), map(str.split, input_data))
    )

    return sum(map(get_prev_history, histories))


input_file = "input.txt"

with open(input_file, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
