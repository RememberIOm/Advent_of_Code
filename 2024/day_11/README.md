# 2024년 Day 11 Advent of Code 문제 풀이

## Part 1

### 문제 설명

Part 1에서는 초기 돌(stone)들의 리스트로 시작하여, 25번의 "깜빡임(blink)" 동안 돌들이 변환되는 과정을 시뮬레이션합니다. 각 깜빡임에서 모든 돌은 다음 규칙에 따라 새로운 돌(들)으로 변환됩니다:

1.  만약 돌의 숫자가 `0`이면, `1`이 됩니다.
2.  만약 돌의 숫자의 자릿수가 짝수이면 (예: 1234), 돌은 두 개의 새로운 돌로 나뉩니다: 앞쪽 절반(12)과 뒤쪽 절반(34).
3.  만약 돌의 숫자의 자릿수가 홀수이면 (예: 123), 돌은 `원래 숫자 * 2024`가 됩니다.

25번의 깜빡임 이후 최종적으로 존재하는 돌의 총 개수를 계산하는 것이 목표입니다.

### 풀이 방법 (`part_1.py`)

1.  **`applicable_rule(stone)` 함수**:
    *   단일 `stone`(정수)을 입력받아 위에서 설명된 변환 규칙에 따라 결과 돌(들)을 튜플 형태로 반환합니다.
        *   `stone == 0` -> `(1,)`
        *   `stone` 자릿수 짝수 (예: 1234) -> `(12, 34)` (문자열로 변환 후 분할, 다시 정수로 변환)
        *   `stone` 자릿수 홀수 (예: 123) -> `(123 * 2024,)`

2.  **`solution(input_data)` 함수**:
    *   입력 데이터의 첫 번째 줄에서 초기 돌들의 리스트 `stones`를 파싱합니다.
    *   `blinks` 리스트를 생성하고, 첫 번째 요소로 초기 `stones` 리스트를 추가합니다. `blinks`는 각 깜빡임 단계에서의 돌 상태(리스트)를 저장하는 리스트입니다.
    *   **시뮬레이션 루프**: `blinks` 리스트의 길이가 26이 될 때까지 (초기 상태 + 25번 깜빡임) 다음을 반복합니다:
        *   `new_stones` 리스트를 새로 생성합니다.
        *   이전 깜빡임 상태(`blinks[-1]`)의 각 `stone`에 대해 `applicable_rule(stone)`을 호출합니다.
        *   `applicable_rule`이 반환한 돌(들)을 `new_stones` 리스트에 `extend`를 사용하여 추가합니다.
        *   완성된 `new_stones` 리스트를 `blinks` 리스트에 추가합니다.
    *   25번의 깜빡임 후, `blinks` 리스트의 마지막 요소(`blinks[-1]`, 즉 26번째 상태)에 포함된 돌의 총 개수(`len(blinks[-1])`)를 반환합니다.

## Part 2

### 문제 설명

Part 2는 Part 1과 동일한 돌 변환 규칙을 따르지만, 훨씬 더 많은 단계(75번의 "깊이" 또는 "세대")까지의 변환 결과를 고려합니다. 각 초기 돌에서 시작하여, 75세대에 도달했을 때 총 몇 개의 "최종" 돌이 생성되는지를 계산하고, 모든 초기 돌에서 생성된 최종 돌들의 총합을 구하는 것이 목표입니다. Part 1처럼 모든 중간 단계를 시뮬레이션하는 것은 비효율적일 수 있습니다.

### 풀이 방법 (`part_2.py`)

1.  **`THRESHOLD = 75`**: 재귀 호출의 최대 깊이를 정의하는 상수입니다. 이 깊이에 도달한 돌은 하나의 "최종" 돌로 간주됩니다.

2.  **`applicable_rule(stone, depth=0)` 함수 (재귀 및 메모이제이션)**:
    *   `@cache` 데코레이터 (`from functools import cache`): 이 함수의 결과를 메모이제이션합니다. 동일한 `(stone, depth)` 쌍으로 함수가 다시 호출되면, 이전에 계산된 결과를 즉시 반환하여 중복 계산을 방지합니다. 이는 성능에 매우 중요합니다.
    *   **기저 조건 (Base Case)**: `if depth == THRESHOLD: return 1`
        *   현재 재귀 깊이가 `THRESHOLD`(75)에 도달하면, 이 경로는 하나의 최종 돌을 생성한 것으로 간주하고 `1`을 반환합니다.
    *   **변환 규칙 (재귀 호출)**:
        *   `stone == 0`: `applicable_rule(1, depth + 1)`을 호출하여 돌 `1`에 대해 다음 깊이에서 재귀적으로 계산합니다.
        *   `stone` 자릿수 짝수: 돌을 두 부분 `first_half`와 `second_half`로 나눕니다. `applicable_rule(first_half, depth + 1) + applicable_rule(second_half, depth + 1)`를 호출하여 각 부분에서 생성될 최종 돌의 수를 합산합니다.
        *   `stone` 자릿수 홀수: `applicable_rule(stone * 2024, depth + 1)`을 호출하여 변환된 돌에 대해 다음 깊이에서 재귀적으로 계산합니다.
    *   계산된 결과 (현재 `stone`과 `depth`에서 시작하여 `THRESHOLD` 깊이까지 도달하는 최종 돌의 총 개수)를 반환합니다.

3.  **`solution(input_data)` 함수**:
    *   입력 데이터에서 초기 돌들의 리스트 `stones`를 파싱합니다.
    *   각 초기 `stone`에 대해 `applicable_rule(stone)` (초기 호출 시 `depth`는 0)을 호출합니다.
    *   각 초기 돌로부터 생성되는 최종 돌들의 총 개수를 모두 합산하여 반환합니다.

이 재귀적 접근 방식과 메모이제이션을 통해, Part 2는 매우 많은 수의 잠재적 변환 경로를 효율적으로 탐색하고 각 초기 돌이 75세대 후에 몇 개의 돌로 이어지는지를 계산합니다.