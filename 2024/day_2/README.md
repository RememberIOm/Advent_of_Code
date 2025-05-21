# 2024년 Day 2 Advent of Code 문제 풀이

## 공통 함수: `is_safe(nums)`

Part 1과 Part 2 솔루션 모두 이 함수를 공통으로 사용합니다.

*   **목적**: 주어진 숫자 시퀀스 `nums` (튜플)가 특정 "안전" 규칙을 만족하는지 확인합니다.
*   **규칙**:
    1.  **단조성(Monotonicity)**: 시퀀스는 전체적으로 엄격하게 증가하거나 엄격하게 감소해야 합니다.
        *   시퀀스의 첫 번째 숫자와 마지막 숫자를 비교하여 전체적인 순서(증가 또는 감소)를 결정합니다 (`order = nums[-1] - nums[0]`).
        *   모든 인접한 숫자 간의 차이(`diff = nums[i+1] - nums[i]`)는 이 전체적인 순서와 일치해야 합니다.
            *   전체가 증가 순서(`order > 0`)이면, 모든 `diff`는 양수여야 합니다 (`diff > 0`).
            *   전체가 감소 순서(`order < 0`)이면, 모든 `diff`는 음수여야 합니다 (`diff < 0`).
            *   `diff * order <= 0` 조건은 `diff`가 0이거나 전체 순서와 반대 방향인 경우를 감지하여 안전하지 않다고 판단합니다.
    2.  **차이의 범위**: 인접한 두 숫자 간의 차이(`diff`)의 절댓값은 1, 2, 또는 3 중 하나여야 합니다. 즉, `1 <= abs(diff) <= 3` 이어야 합니다.
        *   코드는 `if not (-3 <= diff <= 3) or diff == 0:`로 이를 확인합니다. `diff == 0` (인접한 숫자가 동일함)은 안전하지 않습니다.

*   **반환 값**: 시퀀스가 모든 규칙을 만족하면 `True`를, 그렇지 않으면 `False`를 반환합니다.

## Part 1

### 문제 설명

Part 1에서는 여러 줄의 숫자 시퀀스가 입력으로 주어집니다. 각 시퀀스가 위에서 설명된 `is_safe` 함수의 규칙을 만족하는지 확인하여, "안전한" 시퀀스의 총 개수를 계산하는 것이 목표입니다.

### 풀이 방법 (`part_1.py`)

1.  **입력 데이터 파싱 (`solution` 함수 내)**:
    *   입력 데이터 (`input_data`)는 각 줄이 공백으로 구분된 숫자들로 이루어진 문자열 리스트입니다.
    *   각 줄을 파싱하여 정수들의 튜플로 변환합니다. 이 튜플들의 생성기(generator) `lines`가 만들어집니다.

2.  **안전한 시퀀스 필터링 (`solution` 함수 내)**:
    *   `filter(is_safe, lines)`를 사용하여 `lines` 생성기의 각 숫자 시퀀스에 `is_safe` 함수를 적용합니다.
    *   `is_safe` 함수가 `True`를 반환하는 시퀀스들만 필터링하여 `safe_lines` 튜플에 저장합니다.

3.  **결과 반환 (`solution` 함수 내)**:
    *   `len(safe_lines)`를 반환하여 "안전한" 시퀀스의 총 개수를 구합니다.

## Part 2

### 문제 설명

Part 2에서는 "안전" 조건이 좀 더 완화됩니다. 각 숫자 시퀀스는 다음 중 하나의 조건을 만족하면 됩니다:
1.  원본 시퀀스 자체가 `is_safe` 함수의 규칙을 만족한다.
2.  또는, 원본 시퀀스에서 정확히 하나의 숫자를 제거했을 때, 결과로 나오는 수정된 시퀀스가 `is_safe` 함수의 규칙을 만족한다.

이러한 조건을 만족하는 시퀀스의 총 개수를 계산하는 것이 목표입니다.

### 풀이 방법 (`part_2.py`)

1.  **`is_safe(nums)` 함수**: Part 1과 동일하게 사용됩니다.

2.  **`checking(nums)` 함수**:
    *   주어진 숫자 시퀀스 `nums`를 입력으로 받습니다.
    *   먼저, `is_safe(nums)`를 호출하여 원본 시퀀스가 안전한지 확인합니다. 만약 안전하면 즉시 `True`를 반환합니다.
    *   원본 시퀀스가 안전하지 않다면, 시퀀스에서 각 숫자를 한 번씩 제거해보며 수정된 시퀀스가 안전한지 확인합니다:
        *   `for i in range(len(nums))`: `nums`의 각 인덱스 `i`에 대해 반복합니다.
        *   `nums[:i] + nums[i+1:]`: 인덱스 `i`의 요소를 제거한 새로운 튜플을 생성합니다.
        *   `is_safe(...)`를 호출하여 이 수정된 시퀀스가 안전한지 확인합니다.
        *   만약 수정된 시퀀스가 안전하면, `checking` 함수는 `True`를 반환합니다.
    *   원본 시퀀스도 안전하지 않고, 어떤 숫자를 하나 제거해도 안전한 시퀀스를 만들 수 없다면, `False`를 반환합니다.

3.  **`solution(input_data)` 함수**:
    *   입력 데이터 파싱은 Part 1과 동일합니다.
    *   `filter(checking, lines)`를 사용하여 각 숫자 시퀀스에 `checking` 함수를 적용합니다.
    *   `checking` 함수가 `True`를 반환하는 시퀀스들만 필터링합니다.
    *   필터링된 시퀀스들의 총 개수를 반환합니다.The `README.md` file for `2024/day_2/` did not exist.
I have read and understood the logic for `part_1.py` and `part_2.py`.

-   **Shared Function `is_safe(nums)`:** Determines if a sequence of numbers is "safe". A sequence is safe if it's strictly monotonic (all increasing or all decreasing) AND the absolute difference between any two adjacent numbers is between 1 and 3 (inclusive).
-   **Part 1:** Counts how many input sequences are directly "safe" according to `is_safe()`.
-   **Part 2:** Counts how many input sequences satisfy a modified condition: either the original sequence is "safe", OR it becomes "safe" after removing exactly one number from it. This is checked by the `checking(nums)` function which utilizes `is_safe()`.

I have now created the `2024/day_2/README.md` file with detailed explanations of both solutions in Korean, including problem descriptions, the logic of the common `is_safe` function, and the specific approaches for Part 1 and Part 2. Markdown formatting is included.
