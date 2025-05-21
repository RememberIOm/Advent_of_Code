# 2023년 Day 11 Advent of Code 문제 풀이

## Part 1

### 문제 설명

Part 1 문제의 목표는 우주 공간에 있는 은하들의 목록을 입력으로 받아, 모든 은하 쌍 간의 최단 경로 길이를 합산하는 것입니다. 우주 공간은 특정 규칙에 따라 팽창합니다: 완전히 비어 있는 행이나 열은 그 두께가 두 배로 늘어납니다. 최단 경로는 맨해튼 거리(상하좌우 이동만 고려)로 계산됩니다.

### 풀이 방법

`part_1.py` 코드는 다음 단계를 통해 문제를 해결합니다.

1.  **입력 처리 및 그래프 표현**:
    *   입력된 텍스트 데이터를 `numpy` 배열로 변환합니다. 빈 공간 (`.`)은 `0`으로, 은하 (`#`)는 `1`로 표현됩니다.

2.  **우주 팽창**:
    *   먼저, 모든 요소가 `0`인 행(완전히 비어 있는 행)을 찾습니다.
    *   `numpy.all(space == 0, axis=1)`을 사용하여 이러한 행들을 식별합니다.
    *   마찬가지로, 모든 요소가 `0`인 열(완전히 비어 있는 열)을 찾습니다 (`axis=0` 사용).
    *   `numpy.insert()` 함수를 사용하여 식별된 각 빈 행의 위치 바로 다음에 `0`으로 채워진 새로운 행을 삽입합니다. 이는 해당 빈 행의 두께를 효과적으로 두 배로 만듭니다. 빈 열에 대해서도 동일한 작업을 수행합니다.

3.  **은하 위치 식별**:
    *   팽창된 `space` 배열에서 값이 `1`인 모든 셀의 좌표 (행, 열)를 찾습니다. `numpy.where(space == 1)`이 사용됩니다.
    *   이 좌표들은 은하들의 위치를 나타내며, 튜플의 리스트 형태로 저장됩니다.

4.  **최단 경로 계산 및 합산**:
    *   `itertools.combinations(galaxies, 2)`를 사용하여 모든 가능한 고유 은하 쌍을 생성합니다.
    *   각 은하 쌍 `(g1, g2)`에 대해 `get_manhattan_distance(g1, g2)` 함수를 호출하여 맨해튼 거리를 계산합니다. 맨해튼 거리는 `abs(g1_행 - g2_행) + abs(g1_열 - g2_열)`로 계산됩니다.
    *   계산된 모든 맨해튼 거리의 총합을 반환합니다.

## Part 2

### 문제 설명

Part 2는 Part 1과 유사하지만, 팽창 규칙이 다릅니다. 완전히 비어 있는 행이나 열은 이제 백만 배 (1,000,000배) 더 커집니다. 다른 모든 규칙은 동일하게 유지됩니다: 모든 은하 쌍 간의 최단 맨해튼 거리의 합을 계산해야 합니다.

### 풀이 방법

`part_2.py` 코드는 매우 큰 팽창 계수를 효율적으로 처리하기 위해 Part 1과는 다른 접근 방식을 사용합니다. 실제 크기가 백만 배인 배열을 만드는 대신, 거리 계산 시 팽창을 고려하는 방식을 사용합니다.

1.  **입력 처리 및 초기 상태**:
    *   Part 1과 마찬가지로 입력을 `0` (빈 공간)과 `1` (은하)로 구성된 `numpy` 배열(`space`)로 변환합니다.

2.  **팽창 값 정의 및 빈 공간 식별**:
    *   `EXPAND_SIZE = 1_000_000 - 1`로 설정됩니다. 이는 빈 행/열이 기존 크기에 더해 추가되는 크기를 나타냅니다 (즉, 원래 크기 1 + `EXPAND_SIZE` = 1,000,000배).
    *   원래 `space` 배열에서 완전히 비어 있는 행과 열의 인덱스를 식별합니다.

3.  **특수 `space` 배열 구성**:
    *   `numpy.insert()`를 사용하여 식별된 각 원래 빈 행의 인덱스에 `EXPAND_SIZE` 값으로 채워진 *새로운 행*을 삽입합니다. 빈 열에 대해서도 유사하게 `EXPAND_SIZE`로 채워진 *새로운 열*을 삽입합니다.
    *   이 과정 후 `space` 배열은 다음을 포함하게 됩니다:
        *   `1`: 원래 은하의 위치 (새로운 좌표로 이동됨).
        *   `0`: 원래 빈 공간이었던 셀 (새로운 좌표로 이동됨).
        *   `EXPAND_SIZE`: 팽창을 나타내기 위해 삽입된 특수 행/열의 셀.

4.  **`distance_map` 생성**:
    *   위에서 수정된 `space` 배열을 복사하여 `distance_map`을 만듭니다.
    *   `distance_map`에서 값이 `0`인 모든 셀(원래 빈 공간)을 `1`로 변경합니다.
    *   이제 `distance_map`은 각 셀을 통과하는 "비용"을 나타냅니다:
        *   원래 은하였던 셀 또는 원래 빈 공간이었던 셀: 비용 `1`.
        *   팽창으로 인해 삽입된 특수 행/열의 셀: 비용 `EXPAND_SIZE`.

5.  **은하 좌표 업데이트**:
    *   특수 `space` 배열 (삽입 작업 후)에서 은하(`1`)들의 새 좌표를 찾습니다.

6.  **사용자 정의 맨해튼 거리 계산**:
    *   `get_manhattan_distance(g1, g2, distance_map)` 함수는 두 은하 `g1`, `g2`와 `distance_map`을 사용하여 거리를 계산합니다.
    *   두 은하 간의 맨해튼 경로는 수직 이동과 수평 이동으로 구성됩니다.
    *   경로상의 각 셀을 지날 때마다 해당 셀의 `distance_map` 값을 가져와 합산합니다.
        *   일반 셀(원래 은하 또는 빈 공간)을 지나면 비용 `1`이 추가됩니다.
        *   `EXPAND_SIZE` 값을 가진 특수 팽창 마커 셀을 지나면 비용 `EXPAND_SIZE`가 추가됩니다.
    *   결과적으로, 완전히 비어 있던 원래의 행이나 열을 가로지르는 경로는 (원래 두께에 해당하는 비용 `1`) + (팽창된 부분에 해당하는 비용 `EXPAND_SIZE`) = `1 + (1,000,000 - 1)` = `1,000,000`의 비용이 됩니다. 이는 문제의 요구사항과 일치합니다.

7.  **총합 계산**:
    *   모든 은하 쌍에 대해 계산된 이 사용자 정의 맨해튼 거리들의 총합을 반환합니다.

이 방식은 실제로 거대한 배열을 메모리에 생성하지 않고도 큰 팽창 효과를 정확하게 시뮬레이션하여 효율적으로 문제를 해결합니다.Okay, I have created the `README.md` file for `2023/day_11/` with the detailed explanations for `part_1.py` and `part_2.py` in Korean.

The README includes:
- A description of the problem each part is trying to solve.
- A step-by-step explanation of the algorithm and logic used in the Python code.
- How Part 1 handles expansion by literally inserting rows/columns.
- How Part 2 handles massive expansion by inserting "marker" rows/columns with a special value (`EXPAND_SIZE`) and using a custom distance calculation that sums costs from a `distance_map`. This map assigns a cost of 1 to regular cells and `EXPAND_SIZE` to marker cells, effectively simulating the million-fold expansion without creating a giant array.
- Appropriate markdown formatting.
