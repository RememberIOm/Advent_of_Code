# 2024년 Day 10 Advent of Code 문제 풀이

## 문제 설명 (Part 1 및 Part 2 공통)

제공된 `part_1.py`와 `part_2.py`의 코드가 동일하므로, 두 파트 모두 동일한 문제를 해결하는 것으로 보입니다.

문제는 지형도에서 특정 경로를 찾는 것입니다. 지형은 각 지점의 높이(0부터 9까지의 정수)로 주어집니다.
1.  높이가 0인 모든 지점을 시작점으로 간주합니다.
2.  각 시작점에서부터 경로를 탐색합니다. 경로는 현재 지점에서 인접한(상, 하, 좌, 우) 지점으로 이동하며, 이동하려는 다음 지점의 높이가 현재 지점의 높이보다 정확히 1만큼 커야 합니다.
3.  이러한 규칙을 따르는 경로가 높이 9인 지점에 도달하면, 이는 유효한 "종료 지점"에 도달한 것으로 간주합니다.
4.  각 시작점에서 출발하여 도달할 수 있는 높이 9 지점까지의 유효한 경로들의 총 개수를 계산하는 것이 목표입니다. (만약 한 시작점에서 여러 경로를 통해 같은 높이 9 지점에 도달하거나, 여러 다른 높이 9 지점에 도달하는 경우, 각 성공적인 도달을 카운트합니다.)

## 풀이 방법 (Part 1 및 Part 2 공통)

`part_1.py`와 `part_2.py`의 `solution` 함수는 다음 단계를 통해 문제를 해결합니다.

1.  **`get_adjacent_points(point)` 함수**:
    *   주어진 `point` (x, y 좌표 튜플)에 대해 상, 하, 좌, 우 인접 지점들의 좌표 튜플을 반환합니다.

2.  **입력 데이터 파싱 및 초기화 (`solution` 함수 내)**:
    *   입력 데이터 (`input_data`)는 각 줄이 지형의 한 행을 나타내는 문자열 리스트입니다. 각 문자는 해당 지점의 높이입니다.
    *   `topographic_map`: 딕셔너리로, `(x, y)` 좌표를 키로 하고 해당 지점의 정수 높이를 값으로 저장합니다.
    *   `start_points`: 높이가 0인 모든 지점의 `(x, y)` 좌표를 저장하는 리스트입니다.
    *   입력 데이터를 순회하며 `topographic_map`을 채우고 `start_points`를 식별합니다.
    *   `end_point_count`: 최종적으로 반환할, 높이 9 지점에 도달한 경로의 총 개수를 저장할 변수이며 0으로 초기화됩니다.

3.  **각 시작점에서 경로 탐색 (`solution` 함수 내)**:
    *   `start_points` 리스트의 각 `start_point`에 대해 다음을 수행합니다:
        *   `progress_points`: BFS(너비 우선 탐색)와 유사한 방식으로 현재 탐색 중인 경로의 끝 지점들을 저장하는 `deque`입니다. 현재 `start_point`로 초기화됩니다.
        *   `end_point`: 현재 `start_point`에서 시작하여 도달한 높이 9 지점들을 저장하는 리스트입니다. (Part 1 코드에서는 `set`을 사용하여 중복을 자동 제거하지만, Part 2 코드에서는 `list`를 사용합니다. 최종적으로 `len()`을 사용하므로, 각 도달 횟수를 세는 결과는 유사할 수 있습니다.)
        *   **BFS 방식의 탐색 루프**: `progress_points`가 빌 때까지 다음을 반복합니다.
            *   `progress_points`에서 현재 지점 `point`를 꺼냅니다.
            *   `get_adjacent_points(point)`를 사용하여 인접 지점들을 가져옵니다.
            *   각 `adjacent_point`에 대해:
                *   맵 범위 내에 있는지 확인합니다 (`topographic_map`에 키가 있는지 확인).
                *   현재 지점의 높이 `cur_height`와 인접 지점의 높이 `adj_height`를 가져옵니다.
                *   **경로 조건 확인**: `adj_height - cur_height == 1`인지 확인합니다.
                    *   조건이 참이면, 유효한 이동입니다.
                        *   만약 `adj_height == 9`이면, 이 경로는 높이 9의 종료 지점에 도달한 것이므로 `adjacent_point`를 `end_point` 리스트(또는 세트)에 추가합니다.
                        *   만약 `adj_height`가 9가 아니면, 이 경로는 계속 이어질 수 있으므로 `adjacent_point`를 `progress_points` 큐에 추가하여 나중에 탐색하도록 합니다.
        *   현재 `start_point`에서 시작된 모든 경로 탐색이 끝나면, `len(end_point)` (해당 시작점에서 도달한 높이 9 지점의 수)를 `end_point_count`에 더합니다.

4.  **결과 반환**:
    *   모든 `start_points`에 대한 처리가 완료된 후, 최종 `end_point_count` 값을 반환합니다.

이 코드는 각 높이 0 지점에서 시작하여, 높이가 정확히 1씩 증가하는 모든 가능한 경로를 탐색하고, 그중 높이 9에 도달하는 경로의 수를 세는 방식으로 동작합니다.The `README.md` file for `2024/day_10/` did not exist.
I have read and analyzed the solution files `part_1.py` and `part_2.py` and found them to be identical.

The logic involves:
1.  Parsing a grid of heights, identifying all starting points (height 0).
2.  For each starting point, performing a BFS-like traversal.
3.  A path can extend from a current point to an adjacent point if the adjacent point's height is exactly 1 greater than the current point's height.
4.  Counting how many such paths terminate at a cell with height 9.
5.  Summing these counts for all starting points.

I have now created the `2024/day_10/README.md` file with a detailed explanation of this common solution in Korean, including problem description, algorithmic approach, and markdown formatting. Since both Python files are the same, the explanation covers both under a "Part 1 및 Part 2 공통" heading.
