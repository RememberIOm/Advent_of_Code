from enum import IntEnum
from collections import deque
from PIL import Image
import numpy as np


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


def get_inner_num(graph):
    start_y, start_x = get_start_point(graph)

    search_q = deque()
    search_q.append((start_y, start_x, 0))

    loops = tuple([False] * len(graph[0]) for _ in range(len(graph)))
    loops[start_y][start_x] = True

    near_inners = tuple([False] * len(graph[0]) for _ in range(len(graph)))

    while search_q:
        cur_y, cur_x, cur_step = search_q.popleft()

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
            if loops[next_y][next_x]:
                continue

            # 파이프를 loops에 표시
            loops[next_y][next_x] = True

            # 현재 파이프와 이후 파이프의 오른쪽 픽셀을 near_inners에 표시
            for y, x in ((cur_y, cur_x), (next_y, next_x)):
                near_inners[y + (d == direction.RIGHT) - (d == direction.LEFT)][
                    x + (d == direction.UP) - (d == direction.DOWN)
                ] = True

            search_q.append((next_y, next_x, cur_step + 1))

            # 시작할 때 bfs 탐색을 한 쪽으로만 진행하도록 함
            break

    near_inners_image = np.array(near_inners, dtype=np.uint8)
    loops_image = np.array(loops, dtype=np.uint8)

    rgb_image = np.zeros(
        (near_inners_image.shape[0], near_inners_image.shape[1], 3), dtype=np.uint8
    )

    rgb_image[near_inners_image == 1] = [255, 0, 0]  # red
    rgb_image[loops_image == 1] = [255, 255, 255]  # white

    Image.fromarray(rgb_image).save("2023/day_10/fill_before.png")

    # 이후 포토샵으로 답을 구함


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

    get_inner_num(graph)


input_file = "input.txt"

with open(input_file, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

solution(data)
