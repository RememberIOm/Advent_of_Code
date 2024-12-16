from collections import deque


def get_price(position, value, maps, visited, DERIVATIVES):
    edges, area = [], set((position,))
    progress = deque([(position, value)])
    visited.add(position)

    while progress:
        (x, y), value = progress.popleft()

        for dx, dy in DERIVATIVES:
            new_position = (x + dx, y + dy)
            new_value = maps.get(new_position)

            if new_value == value and new_position not in visited:
                progress.append((new_position, new_value))
                visited.add(new_position)
                area.add(new_position)
            elif new_value != value:
                edges.append(new_position)

    return len(edges) * len(area)


def solution(input_data):
    maps = {
        (x, y): value
        for y, line in enumerate(input_data)
        for x, value in enumerate(line)
    }

    DERIVATIVES = ((1, 0), (0, 1), (-1, 0), (0, -1))
    visited = set()
    price = []

    for position, value in maps.items():
        if position in visited:
            continue

        price.append(get_price(position, value, maps, visited, DERIVATIVES))

    return sum(price)


if __name__ == "__main__":
    INPUT_FILE_PATH = "input.txt"

    with open(INPUT_FILE_PATH, "r") as file:
        data = [line.rstrip() for line in file]

    print(solution(data))
