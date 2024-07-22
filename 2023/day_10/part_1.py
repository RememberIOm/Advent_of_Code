from enum import IntEnum
from collections import deque


class direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


def get_start_point(graph):
    for y, row in enumerate(graph):
        for x, pipe in enumerate(row):
            if pipe == 0b1111:
                return y, x


def get_farthest_step(graph):
    start_y, start_x = get_start_point(graph)

    bfs_q = deque()
    bfs_q.append((start_y, start_x, 0))

    visited = tuple([False] * len(graph[0]) for _ in range(len(graph)))
    visited[start_y][start_x] = True

    max_step = 0

    while bfs_q:
        cur_y, cur_x, cur_step = bfs_q.popleft()

        max_step = max(max_step, cur_step)

        for d in direction:
            # 내가 d로 나갈 수 있는지
            if not graph[cur_y][cur_x] & (1 << d):
                continue

            next_y = cur_y + (d == direction.DOWN) - (d == direction.UP)
            next_x = cur_x + (d == direction.RIGHT) - (d == direction.LEFT)

            # idx 탈출 체크
            if not (0 <= next_y < len(graph) and 0 <= next_x < len(graph[0])):
                continue

            # 상대가 d를 통해 들어올 수 있는지
            if not graph[next_y][next_x] & (1 << (d ^ 1)):
                continue

            # 방문 체크
            if visited[next_y][next_x]:
                continue

            visited[next_y][next_x] = True
            bfs_q.append((next_y, next_x, cur_step + 1))

    return max_step


def solution(input_data):
    x_len = len(input_data[0])
    y_len = len(input_data)

    graph = tuple([0] * x_len for _ in range(y_len))

    for y, row in enumerate(input_data):
        for x, pipe in enumerate(row):
            for string, value in zip(
                "|-LJ7F.S",
                (
                    1 << direction.UP | 1 << direction.DOWN,
                    1 << direction.LEFT | 1 << direction.RIGHT,
                    1 << direction.UP | 1 << direction.RIGHT,
                    1 << direction.UP | 1 << direction.LEFT,
                    1 << direction.DOWN | 1 << direction.LEFT,
                    1 << direction.DOWN | 1 << direction.RIGHT,
                    0,
                    1 << direction.UP
                    | 1 << direction.DOWN
                    | 1 << direction.LEFT
                    | 1 << direction.RIGHT,
                ),
            ):
                if pipe == string:
                    graph[y][x] = value
                    break

    return get_farthest_step(graph)


input_file = "input.txt"

with open(input_file, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
