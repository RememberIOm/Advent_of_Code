def cal_seed(seed, layer_element):
    processed_seed = []
    unprocessed_seed = []

    seed_min, seed_max = seed[0], seed[0] + seed[1]
    layer_element_min, layer_element_max = (
        layer_element[1],
        layer_element[1] + layer_element[2],
    )

    layer_element_delta = layer_element[0] - layer_element[1]

    # 모두 포함
    if layer_element_min <= seed_min and seed_max <= layer_element_max:
        processed_seed.append((seed[0] + layer_element_delta, seed[1]))
    # 모두 비포함
    elif seed_max < layer_element_min or layer_element_max < seed_min:
        unprocessed_seed.append(seed)
    # 일부 포함
    else:
        if seed_min < layer_element_min:
            unprocessed_seed.append((seed[0], layer_element_min - seed[0]))

        if layer_element_max < seed_max:
            unprocessed_seed.append((layer_element_max, seed_max - layer_element_max))

        processed_seed.append(
            (
                max(seed_min, layer_element_min) + layer_element_delta,
                min(seed_max, layer_element_max) - max(seed_min, layer_element_min),
            )
        )

    return processed_seed, unprocessed_seed


def cal_range(seeds, layer):
    processed_seeds = []

    for seed in seeds:
        unprocessed_seeds = (seed,)
        next_unprocessed_seeds = []

        for layer_element in layer:
            for unprocessed_seed in unprocessed_seeds:
                processed_seed, unprocessed_seed = cal_seed(
                    unprocessed_seed, layer_element
                )
                processed_seeds.extend(processed_seed)
                next_unprocessed_seeds.extend(unprocessed_seed)

            unprocessed_seeds = next_unprocessed_seeds
            next_unprocessed_seeds = []

        processed_seeds.extend(unprocessed_seeds)

    return processed_seeds


def cal_seeds(seeds, layers):
    for layer in layers:
        seeds = cal_range(seeds, layer)

    return seeds


def solution(input_data):
    seeds = tuple(map(int, input_data[0].split(": ")[1].split()))
    seeds = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]

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

    seeds.sort()

    return seeds[0][0]


input_file = "input.txt"

with open(input_file, "r") as file:
    data = list(map(str.rstrip, file.readlines()))

print(solution(data))
