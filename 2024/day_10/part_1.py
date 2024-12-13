from collections import deque


def get_adjacent_points(point):
    x, y = point

    return (x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)


def solution(input_data):
    topographic_map = {}
    start_points = []

    for y, row in enumerate(input_data):
        for x, height in enumerate(row):
            height = int(height)

            topographic_map[(x, y)] = height
            if height == 0:
                start_points.append((x, y))

    end_point_count = 0

    for start_point in start_points:
        progress_points = deque([start_point])
        end_point = set()

        while progress_points:
            point = progress_points.popleft()

            for adjacent_point in get_adjacent_points(point):
                if adjacent_point not in topographic_map:
                    continue

                cur_height = topographic_map[point]
                adj_height = topographic_map[adjacent_point]

                if adj_height - cur_height == 1:
                    if adj_height == 9:
                        end_point.add(adjacent_point)
                    else:
                        progress_points.append(adjacent_point)

        end_point_count += len(end_point)

    return end_point_count


if __name__ == "__main__":
    INPUT_FILE_PATH = "input.txt"

    with open(INPUT_FILE_PATH, "r") as file:
        data = [line.rstrip() for line in file]

    print(solution(data))
