def is_include(seed, layer_element):
    return layer_element[1] <= seed <= layer_element[1] + layer_element[2]


def cal_seed(seed, layer):
    for layer_element in layer:
        if is_include(seed, layer_element):
            return seed + layer_element[0] - layer_element[1]

    return seed


def cal_seeds(seeds, layers):
    for layer in layers:
        seeds = tuple(map(lambda seed: cal_seed(seed, layer), seeds))

    return seeds


def solution(input_data):
    seeds = list(map(int, input_data[0].split(": ")[1].split()))

    idx_list = []

    for i, line in enumerate(input_data):
        for start_string in (
            "seed-",
            "soil-",
            "fertilizer-",
            "water-",
            "light-",
            "temperature-",
            "humidity-",
        ):
            if line.startswith(start_string):
                idx_list.append(i)
                break

    idx_list.append(len(input_data))

    layers = []

    for head, tail in zip(idx_list, idx_list[1:]):
        layers.append(
            tuple(tuple(map(int, i.split())) for i in input_data[head + 1 : tail - 1])
        )

    seeds = cal_seeds(seeds, layers)

    return min(seeds)


input_file = "input.txt"

with open(input_file, "r") as file:
    data = list(map(str.rstrip, file.readlines()))

print(solution(data))
