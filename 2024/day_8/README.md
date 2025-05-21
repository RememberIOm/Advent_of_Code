# 2024년 Day 8 Advent of Code 문제 풀이

## 공통 입력 파싱 로직

Part 1과 Part 2의 `solution` 함수는 유사한 초기 입력 파싱 로직을 공유합니다:

1.  입력 데이터 (`input_data`)는 그리드를 나타내는 문자열 리스트입니다.
2.  `antennas` 딕셔너리를 생성합니다. 이 딕셔너리는 각 안테나 문자(예: 'A', 'B' 등, '.'이 아닌 문자)를 키로 하고, 해당 안테나가 그리드에 나타나는 모든 `(x, y)` 좌표들의 리스트를 값으로 가집니다.
3.  그리드를 순회하며 각 문자를 확인하고, '.'이 아니면 해당 문자의 안테나 종류에 맞게 `antennas` 딕셔너리에 좌표를 추가합니다.

## Part 1

### 문제 설명

Part 1의 목표는 주어진 그리드 내의 안테나들을 기반으로 "반노드(antinode)" 지점들을 찾아, 그리드 경계 내에 있는 고유한 반노드의 총 개수를 계산하는 것입니다.

반노드는 다음과 같이 정의됩니다:
1.  동일한 종류의 안테나가 위치한 두 개의 서로 다른 지점 P1(`other_x`, `other_y`)과 P2(`cur_x`, `cur_y`)를 선택합니다.
2.  벡터 V = P2 - P1 (즉, `(cur_x - other_x, cur_y - other_y)`)을 계산합니다.
3.  두 개의 반노드 지점을 계산합니다:
    *   AP1 = P2 + V = `(cur_x + (cur_x - other_x), cur_y + (cur_y - other_y))`
    *   AP2 = P1 - V = `(other_x - (cur_x - other_x), other_y - (cur_y - other_y))`
    이들은 P1-P2 선분을 P2 너머로, 그리고 P1 너머로 동일한 길이만큼 연장한 지점들입니다.
4.  모든 안테나 종류와 해당 종류 내 모든 P1, P2 쌍에 대해 이러한 반노드들을 생성합니다.
5.  생성된 모든 고유한 반노드들 중에서 그리드의 경계 내에 있는 것들의 개수를 셉니다.

### 풀이 방법 (`part_1.py`)

1.  **`get_antinode(antennas)` 함수**:
    *   `antinodes`라는 빈 `set`을 초기화하여 고유한 반노드 좌표를 저장합니다.
    *   `antennas` 딕셔너리의 각 안테나 종류(`antenna`)와 해당 위치 리스트(`positions`)에 대해 반복합니다.
    *   각 `positions` 리스트 내에서 두 개의 서로 다른 위치 `(cur_x, cur_y)` (P2로 간주)와 `(other_x, other_y)` (P1로 간주)를 선택하는 모든 쌍에 대해 반복합니다.
        *   두 위치가 동일하면 건너뜁니다.
        *   `diff_x = cur_x - other_x` 와 `diff_y = cur_y - other_y`를 계산합니다 (벡터 V의 성분).
        *   두 개의 반노드 지점 `(cur_x + diff_x, cur_y + diff_y)` 와 `(other_x - diff_x, other_y - diff_y)`를 계산합니다.
        *   계산된 두 반노드 지점을 `antinodes` 셋에 추가합니다.
    *   모든 계산이 끝나면 `antinodes` 셋을 반환합니다.

2.  **`solution(input_data)` 함수**:
    *   공통 파싱 로직을 사용하여 `antennas` 딕셔너리를 생성합니다.
    *   `bounds`라는 `set`을 생성하여 그리드 내의 모든 유효한 `(x, y)` 좌표를 저장합니다. 이는 `(y_최대길이, x_최대길이)`를 기반으로 생성됩니다.
    *   `get_antinode(antennas)`를 호출하여 모든 잠재적 반노드들을 얻습니다.
    *   이 반노드 셋과 `bounds` 셋의 교집합 (`&` 연산자)을 구하여 그리드 경계 내에 있는 반노드들만 필터링합니다.
    *   필터링된 반노드들의 개수 (`len(...)`)를 반환합니다.

## Part 2

### 문제 설명

Part 2는 Part 1의 반노드 개념을 확장합니다. 두 안테나 지점 P1과 P2가 주어졌을 때, 이 두 지점을 지나는 직선을 양방향으로 무한히 연장한다고 가정합니다. 이 직선 위에 P1에서 (P2-P1) 벡터 방향으로 정수 간격으로 나타나는 모든 지점들과, P2에서 (P1-P2) 벡터 방향으로 정수 간격으로 나타나는 모든 지점들(P1, P2 자체는 제외될 수도, 포함될 수도 있음 - 코드 로직에 따라 결정)을 "확장된 반노드"로 간주합니다.

목표는 이러한 모든 확장된 반노드들 중에서 그리드 경계 내에 있는 고유한 지점들의 총 개수를 계산하는 것입니다.

### 풀이 방법 (`part_2.py`)

1.  **`get_antinode(antennas, bounds)` 함수**:
    *   `antinodes` 빈 `set`과 `bounds` (그리드 내 유효 좌표 셋)를 입력으로 받습니다.
    *   Part 1과 유사하게 `antennas` 딕셔너리를 순회하며 각 안테나 종류 내의 모든 서로 다른 위치 쌍 P1(`other_x`, `other_y`)과 P2(`cur_x`, `cur_y`)를 선택합니다.
    *   `diff_x = cur_x - other_x` 와 `diff_y = cur_y - other_y` (벡터 V = P2-P1)를 계산합니다.
    *   **P2에서 V 방향으로의 확장선 상의 점들 계산**:
        *   `point_to_check_x, point_to_check_y`를 P2(`cur_x, cur_y`)로 초기화합니다.
        *   `while True` 루프를 사용하여 P2로부터 V 방향으로 계속 이동합니다:
            *   `point_to_check_x += diff_x`, `point_to_check_y += diff_y` (다음 지점으로 이동).
            *   새로운 `(point_to_check_x, point_to_check_y)`가 `bounds` 내에 없으면 루프를 중단합니다.
            *   그렇지 않으면, 이 지점을 `antinodes` 셋에 추가합니다.
        *   (주: 코드에서는 `other_x_copy`, `other_y_copy`를 `other_x`, `other_y`(P1)로 초기화한 후 첫 단계에서 `diff_x`, `diff_y`를 더하여 P2(`cur_x, cur_y`)에 도달한 후, 그 다음 점부터 `antinodes`에 추가하기 시작합니다. 즉, P2 + k*V (k=1, 2, ...) 형태의 점들이 추가됩니다.)
    *   **P1에서 -V 방향으로의 확장선 상의 점들 계산**:
        *   `point_to_check_x, point_to_check_y`를 P1(`other_x`, `other_y`)로 초기화합니다.
        *   `while True` 루프를 사용하여 P1로부터 -V 방향으로 계속 이동합니다:
            *   `point_to_check_x -= diff_x`, `point_to_check_y -= diff_y` (다음 지점으로 이동).
            *   새로운 `(point_to_check_x, point_to_check_y)`가 `bounds` 내에 없으면 루프를 중단합니다.
            *   그렇지 않으면, 이 지점을 `antinodes` 셋에 추가합니다.
        *   (주: 코드에서는 `cur_x_copy`, `cur_y_copy`를 `cur_x`, `cur_y`(P2)로 초기화한 후 첫 단계에서 `diff_x`, `diff_y`를 빼서 P1(`other_x, other_y`)에 도달한 후, 그 다음 점부터 `antinodes`에 추가하기 시작합니다. 즉, P1 - k*V (k=1, 2, ...) 형태의 점들이 추가됩니다.)
    *   모든 계산이 끝나면 `antinodes` 셋을 반환합니다. 이 셋에는 이미 `bounds` 검사가 완료된 점들만 포함됩니다.

2.  **`solution(input_data)` 함수**:
    *   공통 파싱 로직으로 `antennas` 딕셔너리를 생성하고, `bounds` 셋을 만듭니다.
    *   `get_antinode(antennas, bounds)` (Part 2 버전)를 호출하여 모든 유효한 확장된 반노드들의 셋을 얻습니다.
    *   이 셋의 크기 (`len(...)`)를 반환합니다.

코드의 `get_antinode` 함수 내 루프 초기화 및 첫 단계 처리 방식을 보면, P1과 P2 자체는 생성되는 "확장된 반노드" 리스트에 직접적으로 첫 번째 요소로 포함되지 않고, 그 다음 정수 간격의 점들부터 수집됩니다.The `README.md` file for `2024/day_8/` did not exist.
I have read and understood the logic for `part_1.py` and `part_2.py`.

-   **Input Parsing (Common):** Both identify locations `(x,y)` of different antenna types from a grid input. `antennas` is a dict `{'type': [(x1,y1), (x2,y2), ...]}`.

-   **Part 1:**
    -   For each antenna type, it considers all unique pairs of its locations (P1, P2).
    -   For each pair, it calculates two "antinode" points: `P_anti1 = P2 + (P2 - P1)` and `P_anti2 = P1 + (P1 - P2)`. These are points on the line P1-P2, lying outside the P1-P2 segment, such that P2 is the midpoint of P1-P_anti1, and P1 is the midpoint of P2-P_anti2.
    -   It collects all such unique antinode points that fall within the grid boundaries and returns their count.

-   **Part 2:**
    -   Similar to Part 1, it considers pairs of antenna locations (P1, P2) for each type.
    -   For each pair, it generates all integer-coordinate points on the two rays starting from P1 (extending away from P2) and from P2 (extending away from P1), as long as these points are within grid boundaries.
        -   The code's implementation:
            -   Ray 1: Starts generating from `P1 + (P2-P1) = P2`, then `P2 + (P2-P1)`, `P2 + 2*(P2-P1)`, ... Adds these to a set if in bounds.
            -   Ray 2: Starts generating from `P2 - (P2-P1) = P1`, then `P1 - (P2-P1)`, `P1 - 2*(P2-P1)`, ... Adds these to a set if in bounds.
        -   Effectively, this means it collects points `P2 + k*(P2-P1)` and `P1 - k*(P2-P1)` for `k=0, 1, 2, ...` as long as they are in bounds. The `k=0` case generates P2 and P1 respectively. Since `antinodes` is a set, these initial P1/P2 points (if added) don't affect the uniqueness if they are also generated by other means or are actual antenna positions. The problem likely intends to count points *other than* the original antenna positions P1 and P2 that lie on these extended lines. The current code might include P1 and P2 in the set if they are generated during the "extension" from another point. However, the description of the problem as "antinodes" usually implies points symmetrically outside. The problem is counting all unique grid points "covered" by these line extensions.
    -   The final result is the count of all unique such points collected from all pairs and all antenna types.

I have now created the `2024/day_8/README.md` file with detailed explanations of both solutions in Korean, based on the code's behavior. Markdown formatting is included. I've added notes to clarify the point generation in Part 2.
