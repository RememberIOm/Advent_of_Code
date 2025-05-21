# 2024년 Day 6 Advent of Code 문제 풀이

## Part 1

### 문제 설명

Part 1에서는 로봇이 그리드 내에서 이동하는 경로를 시뮬레이션합니다. 그리드는 빈 공간과 벽('#')으로 구성되며, 로봇은 초기 위치와 방향(예: '^', '>', 'v', '<')을 가집니다.

로봇의 이동 규칙은 다음과 같습니다:
1.  현재 방향으로 한 칸 앞으로 이동합니다.
2.  만약 이동한 칸이 벽('#')이 아니라면, 해당 칸을 방문한 것으로 기록하고 다음 이동을 위해 현재 위치를 업데이트합니다.
3.  만약 이동한 칸이 벽이라면, 로봇은 원래 위치(벽에 부딪히기 직전의 위치)로 후퇴한 다음, 시계 방향으로 90도 회전합니다. 그 후, 새로운 방향으로 한 칸 앞으로 이동합니다. (이때 이동한 칸이 또 벽일 수도 있지만, 문제의 시뮬레이션은 다음 단계에서 이를 처리합니다.)

로봇이 그리드 밖으로 나갈 때까지 이 과정을 반복합니다. 목표는 로봇이 성공적으로 방문한 (즉, 벽이 아니어서 실제로 들어간) 고유한 칸의 총 개수를 세는 것입니다.

### 풀이 방법 (`part_1.py`)

1.  **초기화**:
    *   `directions = "^>v<"`: 이동 방향 문자열 (위, 오른쪽, 아래, 왼쪽 순).
    *   `directions_map`: 각 방향 문자를 실제 좌표 변화 `(행_변화, 열_변화)`로 매핑하는 딕셔너리. 예를 들어, `^`는 `(-1, 0)` (행 인덱스 감소).
    *   입력 그리드 `input_data`를 순회하여 로봇의 시작 위치 `(x, y)` (코드에서는 `i`가 행, `j`가 열이므로 `(행, 열)`로 저장)와 초기 `direction`을 찾습니다.

2.  **시뮬레이션 루프**:
    *   `visited_positions`: 로봇이 성공적으로 방문한 좌표 `(행, 열)`들을 저장하는 `set`이며, 시작 위치로 초기화됩니다.
    *   `while` 루프는 로봇의 현재 위치 `(x, y)`가 그리드 범위 내에 있는 동안 계속됩니다.
    *   **이동 및 상태 업데이트**:
        *   **벽이 아닌 경우**: 현재 로봇이 위치한 `input_data[x][y]`가 벽('#')이 아니면:
            *   현재 위치 `(x, y)`를 `visited_positions`에 추가합니다.
            *   `directions_map`을 참조하여 현재 `direction`으로 한 칸 전진하여 `x`와 `y`를 업데이트합니다.
        *   **벽인 경우**: 현재 로봇이 위치한 `input_data[x][y]`가 벽이면:
            *   먼저, `directions_map`을 사용하여 현재 `direction`의 반대 방향으로 한 칸 이동하여 로봇을 이전 칸(벽에 부딪히기 직전 칸)으로 되돌립니다.
            *   `directions` 문자열에서 현재 `direction`의 인덱스를 찾아 1을 더하고 4로 나눈 나머지를 사용하여 다음 방향(시계방향 90도 회전)을 결정합니다.
            *   새로운 `direction`으로 `directions_map`을 참조하여 한 칸 전진하여 `x`와 `y`를 업데이트합니다.

3.  **결과**:
    *   루프가 종료되면 (로봇이 그리드 밖으로 나가면), `len(visited_positions)`를 반환하여 방문한 고유 칸의 수를 구합니다.

## Part 2

### 문제 설명

Part 2에서는 Part 1과 동일한 로봇 및 이동 규칙을 사용합니다. 하지만 목표는 다릅니다: 그리드 내의 각 빈 공간('.') 위치에 대해, 만약 그 위치에 벽('#')을 하나 설치했을 때 로봇의 경로가 무한 루프에 빠지게 되는 경우가 몇 번인지 세는 것입니다.

루프는 로봇이 이전에 특정 벽 앞에서 특정 방향으로 서 있었던 상태와 동일한 상태(즉, 동일한 위치에서 동일한 방향으로 다시 해당 벽에 막힘)로 돌아올 때 발생하는 것으로 간주합니다.

### 풀이 방법 (`part_2.py`)

1.  **전역 상수 및 좌표계**:
    *   `DIRECTIONS = "^>v<"`
    *   `DIRECTIONS_MAP = [(0, -1), (1, 0), (0, 1), (-1, 0)]`: `(열_변화, 행_변화)` 순서로 정의됩니다. `^` (위)는 `(0, -1)` (행 인덱스 감소). 이는 `grid[y][x]` 접근 방식과 일치합니다.

2.  **`is_loop(grid, start_x, start_y, start_direction)` 함수**:
    *   주어진 `grid` 상태와 로봇의 시작 조건(`start_x`, `start_y`, `start_direction`)에서 로봇의 경로가 루프를 형성하는지 확인합니다.
    *   `visited_positions`: `(x, y, direction)` 튜플을 저장하는 `set`입니다. 여기서 `(x,y)`는 로봇이 벽에 부딪혀 회전하기 직전의 위치이며, `direction`은 해당 벽에 부딪혔을 때의 방향입니다. 이 상태가 반복되면 루프입니다.
    *   **시뮬레이션 루프**:
        *   **벽이 아닌 경우**: Part 1과 유사하게 현재 `direction`으로 전진합니다.
        *   **벽인 경우**:
            *   현재 `direction`의 반대 방향으로 한 칸 후퇴하여 벽 앞 위치 `(x,y)`로 돌아옵니다.
            *   `current_state = (x, y, direction)`을 만듭니다.
            *   만약 `current_state`가 `visited_positions`에 이미 있다면, 루프가 감지된 것이므로 `True`를 반환합니다.
            *   `visited_positions`에 `current_state`를 추가합니다.
            *   방향을 시계방향으로 90도 회전합니다 (`direction = (direction + 1) % 4`).
            *   새로운 방향으로 한 칸 전진합니다.
    *   로봇이 그리드 밖으로 나가면 루프 없이 종료된 것이므로 `False`를 반환합니다.

3.  **`check_loop(args)` 함수**:
    *   멀티프로세싱을 위한 래퍼 함수입니다. `args`는 `(grid, cur_x, cur_y, start_x, start_y, start_direction)`를 포함합니다.
    *   `grid[cur_y][cur_x]` (원래 '.'였던 위치)를 일시적으로 '#'으로 변경합니다.
    *   `is_loop` 함수를 호출하여 루프 발생 여부를 확인합니다.
    *   `grid[cur_y][cur_x]`를 다시 '.'으로 복원합니다.
    *   `is_loop`의 결과를 반환합니다.

4.  **`solution(input_data)` 함수**:
    *   입력 그리드를 수정 가능한 리스트의 리스트 `data_grid`로 변환합니다.
    *   로봇의 초기 `start_x`, `start_y`, `start_direction` (방향은 0-3 인덱스로 변환)을 찾습니다.
    *   `dot_cells`: 그리드에서 원래 '.'이었던 모든 셀의 `(x, y)` 좌표 리스트를 만듭니다.
    *   `tasks`: 각 `dot_cell` 위치에 임시로 벽을 설치하는 시나리오에 대한 인자들을 `check_loop` 함수용으로 준비합니다.
    *   **멀티프로세싱**: `multiprocessing.pool.Pool`을 사용하여 `tasks`에 대해 `check_loop` 함수를 병렬로 실행합니다. `tqdm`을 사용하여 진행 상황을 표시합니다.
    *   각 작업의 결과(루프 발생 여부를 나타내는 boolean 값들의 리스트)를 합산하여 (`True`는 1로, `False`는 0으로 취급) 루프를 발생시키는 벽 설치 경우의 총 수를 반환합니다.The `README.md` file for `2024/day_6/` did not exist.
I have read and understood the logic for `part_1.py` and `part_2.py`.

-   **Part 1:** Simulates a robot moving on a grid. The robot moves forward in its current direction. If it hits a wall ('#'), it retreats, turns 90 degrees right, and then moves forward. The goal is to count the number of unique non-wall cells the robot visits before going out of bounds.
    -   The coordinate system interpretation in `part_1.py` for `directions_map` appears to be `(row_change, col_change)` when accessing `input_data[x][y]` where `x` is row and `y` is column.

-   **Part 2:** Determines how many empty cells ('.') can be turned into a single wall ('#') such that the robot's path (starting from a given initial state) forms a loop. A loop is detected if the robot is about to turn at a wall from a state (position before hitting wall, direction when hitting wall) that it has encountered before.
    -   The coordinate system in `part_2.py` for `DIRECTIONS_MAP` is `(col_change, row_change)` and grid access is `grid[y][x]` where `y` is row and `x` is column. This is a more standard (x,y) interpretation for columns and rows.
    -   It uses multiprocessing to test each possible wall placement.

I have now created the `2024/day_6/README.md` file with detailed explanations of both solutions in Korean. I've noted the coordinate system handling for clarity in the explanations. Markdown formatting is included.
