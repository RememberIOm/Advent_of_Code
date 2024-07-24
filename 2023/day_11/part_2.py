import numpy as np
from itertools import combinations


def get_manhattan_distance(p1, p2, distance_map):
    x_min, x_max = sorted((p1[0], p2[0]))
    y_min, y_max = sorted((p1[1], p2[1]))

    x_route = distance_map[x_min:x_max, y_min]
    y_route = distance_map[x_max, y_min:y_max]

    return x_route.sum() + y_route.sum()


def solution(input_data):
    # 0: 빈 공간, 1: 은하
    space = np.array(
        tuple(tuple(0 if c == "." else 1 for c in line) for line in input_data)
    )

    # 빈 공간이 있는 행과 열을 찾아서 EXPAND_SIZE를 삽입
    EXPAND_SIZE = 1_000_000 - 1

    is_row_empty = np.all(space == 0, axis=1)
    is_col_empty = np.all(space == 0, axis=0)

    space = np.insert(space, np.where(is_row_empty)[0], EXPAND_SIZE, axis=0)
    space = np.insert(space, np.where(is_col_empty)[0], EXPAND_SIZE, axis=1)

    # 모든 1의 위치를 담는 튜플
    galaxies = np.where(space == 1)
    galaxies = tuple(zip(galaxies[0], galaxies[1]))

    # 각 칸의 거리가 저장된 배열
    distance_map = space.copy()
    distance_map[distance_map == 0] = 1

    # 모든 은하 쌍의 거리를 계산
    distances = (
        get_manhattan_distance(g1, g2, distance_map)
        for g1, g2 in combinations(galaxies, 2)
    )

    return sum(distances)


input_file = "input.txt"

with open(input_file, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
