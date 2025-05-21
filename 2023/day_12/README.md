# 2023년 Day 12 Advent of Code 문제 풀이

## Part 1

### 문제 설명

Part 1 문제의 목표는 손상된 스프링 기록의 각 줄을 분석하는 것입니다. 각 줄은 스프링의 상태를 나타내는 문자열(operational `.`, damaged `#`, unknown `?`)과 연속된 손상된 스프링 그룹의 크기를 나타내는 숫자 배열로 구성됩니다. `?`를 `.` 또는 `#`으로 바꾸어 주어진 숫자 배열의 제약 조건을 만족하는 가능한 모든 배열의 수를 계산해야 합니다.

예를 들어, 입력 "???.### 1,1,3"은 세 개의 그룹(크기 1, 1, 3의 손상된 스프링)이 있어야 함을 의미합니다. `?`를 적절히 바꾸어 이 패턴을 만족하는 방법의 수를 찾아야 합니다.

### 풀이 방법 (`part_1.py`)

`part_1.py`의 접근 방식은 가능한 모든 유효한 스프링 구성을 생성한 후, 주어진 `?` 패턴과 일치하는지 확인하는 브루트포스(brute-force) 조합 생성 방법입니다.

1.  **입력 파싱**:
    *   각 줄을 `(broken_spring_string, arrangement_tuple)` 쌍으로 파싱합니다. 예를 들어, "???.### 1,1,3"은 `("???.###", (1,1,3))`이 됩니다.

2.  **`cal_case_num(spring)` 함수**:
    *   주어진 `(broken_spring, arrangement)`에 대해 가능한 배열 수를 계산합니다.
    *   `get_possible_cases(broken_spring, arrangement)`를 호출하여 `arrangement` 숫자와 `broken_spring` 문자열 길이에만 기반한 모든 잠재적 유효 문자열(모든 `?`가 `.` 또는 `#`으로 채워진)을 생성합니다.
    *   생성된 각 `case_string`에 대해 `is_broken_spring_cases(broken_spring, case_string)`를 호출하여 원래 `broken_spring` 문자열의 `?`와 호환되는지 확인합니다.
    *   호환되는 경우의 수를 합산합니다.

3.  **`get_possible_cases(broken_spring, arrangement)` 함수**:
    *   `get_dot_arrangements(broken_spring, arrangement)`를 호출하여 `#` 블록들 사이와 주변에 들어갈 `.`의 개수 조합을 얻습니다.
    *   예를 들어, `arrangement = (1,1)`이고 `dot_arrangement = (1,2,0)` (첫 `#`블록 앞에 `.` 1개, 두 `#`블록 사이에 `.` 2개, 마지막 `#`블록 뒤에 `.` 0개)이면, ".#..#" 문자열을 구성합니다.

4.  **`get_dot_arrangements(broken_spring, arrangement)` 함수**:
    *   이 함수는 `#` 블록들의 총 개수(`arrangement_len`), `#`의 총합(`arrangement_sum`), 그리고 전체 스프링 길이(`broken_spring_len`)를 고려하여 `.`들의 가능한 길이 조합을 생성합니다.
    *   핵심 아이디어는 `#` 블록들 사이에는 최소 1개의 `.`이 있어야 하고, 문자열의 양 끝에는 0개 이상의 `.`이 올 수 있다는 점입니다.
    *   `itertools.combinations_with_replacement`와 `permutations`를 사용하여 `#` 블록들 사이에 위치할 `.`들의 길이를 정하고, 남은 공간을 양 끝의 `.` 길이에 할당합니다.

5.  **`is_broken_spring_cases(broken_spring, case_string)` 함수**:
    *   생성된 `case_string`( `.`과 `#`만 포함)이 원래 `broken_spring` 문자열( `?` 포함)과 일치하는지 확인합니다.
    *   `broken_spring`의 문자가 `?`가 아니고 `case_string`의 해당 문자와 다르면 `False`를 반환합니다. 모두 일치하면 `True`를 반환합니다.

6.  **결과 집계**:
    *   모든 입력 줄에 대해 `cal_case_num`을 호출하고 그 결과를 합산하여 최종 답을 얻습니다.

이 방식은 문제의 크기가 작을 때는 작동하지만, 경우의 수가 많아지면 매우 느려질 수 있습니다.

## Part 2

### 문제 설명

Part 2는 Part 1과 동일한 기본 문제를 다루지만, 입력이 "펼쳐집니다(unfolded)". 각 스프링 문자열은 `?`를 사이에 두고 5번 반복되며, 손상된 스프링 그룹의 숫자 배열도 5번 반복됩니다. 이로 인해 가능한 조합의 수가 기하급수적으로 증가하여 Part 1의 브루트포스 방식은 실용적이지 않게 됩니다.

### 풀이 방법 (`part_2.py`)

`part_2.py`는 동적 프로그래밍(Dynamic Programming, DP)을 사용하여 확장된 문제를 효율적으로 해결합니다.

1.  **입력 펼치기**:
    *   `UNFOLD_SPRING = 5`로 설정합니다.
    *   원래 `broken_spring_string`은 `(original_string + "?") * 5` (마지막 `?`는 제거) 형태로 5번 반복됩니다.
    *   `arrangement_tuple`도 5번 반복됩니다.

2.  **`cal_case_num(spring)` 함수 (DP 핵심 로직)**:
    *   `broken_springs` (문자열)와 `conditions` (숫자 튜플)를 입력으로 받습니다.
    *   **전처리**:
        *   `broken_springs = "_" + broken_springs`: DP 테이블의 경계 조건 처리를 단순화하기 위해 문자열 앞에 더미 문자를 추가합니다.
        *   `conditions = (0,) + conditions`: 조건 배열 앞에도 더미 조건 0을 추가합니다.
        *   `conditions_prefix_sum`: 조건들의 누적 합을 미리 계산하여 특정 조건 그룹까지 필요한 최소 `#` 개수를 빠르게 알 수 있도록 합니다.
        *   `streaks`: `streaks[j]`는 `broken_springs[j]`에서 끝나는 연속된 `.`이 아닌 문자('#' 또는 '?')의 최대 길이를 저장합니다. 이는 현재 위치에서 특정 길이의 `#` 블록을 형성할 수 있는지 확인하는 데 사용됩니다.

    *   **DP 테이블 초기화**:
        *   `dp_table[i][j]`는 `broken_springs` 문자열의 첫 `j`개 문자를 사용하여 `conditions` 배열의 첫 `i`개 조건을 만족시키는 방법의 수를 저장합니다.
        *   `dp_table[0][0] = 1`: 0개의 조건은 0개의 문자(더미 문자 `_`)로 1가지 방법(빈 배열)으로 만족시킬 수 있다는 기본 경우입니다.

    *   **DP 테이블 채우기**:
        *   `i` (조건 인덱스)와 `j` (문자열 인덱스)에 대해 반복합니다.
        *   `min_len_needed = conditions_prefix_sum[i] + i - 1`: `i`번째 조건까지 만족시키기 위해 필요한 최소 문자열 길이 (모든 `#`의 합 + `#` 블록들 사이의 최소 `.` 개수). `j`가 이보다 작으면 현재 상태는 불가능합니다.
        *   **현재 문자 `broken_springs[j]`를 `.`으로 처리하는 경우**:
            *   `broken_springs[j]`가 `#`이 아니라면 (`.` 또는 `?`인 경우), 이 문자를 `.`으로 간주할 수 있습니다.
            *   이 경우, `dp_table[i][j]`에 `dp_table[i][j-1]`의 값을 더합니다. (즉, `j-1`번째 문자까지 `i`개의 조건을 만족한 경우의 수를 가져옴).
        *   **현재 문자 `broken_springs[j]`를 `#`의 일부로 처리하는 경우**:
            *   `broken_springs[j]`가 `.`이 아니라면 (`#` 또는 `?`인 경우), 이 문자를 현재 `cond = conditions[i]` 길이의 `#` 블록의 마지막 문자로 간주할 수 있습니다.
            *   다음 조건들을 확인하여 유효성을 검사합니다:
                1.  `cond == 0`: 현재 조건이 더미 0이면 (실제 `#` 블록이 아님), 이 경로를 고려하지 않습니다.
                2.  `cond > streaks[j]`: `broken_springs[j]`에서 끝나는 연속된 `#` 또는 `?`의 최대 길이가 `cond`보다 작으면, `cond` 길이의 블록을 형성할 수 없습니다.
                3.  `broken_springs[j - cond] == '#'`: `cond` 길이의 블록 바로 앞 문자(`broken_springs[j-cond]`)가 `#`이면, 블록들이 분리되지 않으므로 유효하지 않습니다. (더미 문자 `_` 덕분에 `j-cond`가 0일 때도 안전하게 검사 가능).
            *   위 조건 중 하나라도 참이면, 현재 문자를 `#` 블록의 끝으로 사용할 수 없으므로 다음으로 넘어갑니다.
            *   유효하다면, `cond` 길이의 `#` 블록과 그 앞의 `.` 하나를 사용한 것이므로, `dp_table[i-1][j - cond - 1]`의 값을 `dp_table[i][j]`에 더합니다.
                *   `j - cond - 1 < 0`인 경우 (즉, `#` 블록이 문자열 맨 앞에서 시작하고, `i-1`이 0번째 더미 조건을 가리키는 경우), 이는 `dp_table[0][0]` 즉, 1을 더하는 것과 같습니다. 코드에서는 `else: dp_table[i][j] += 1`로 이 경우를 처리합니다.

    *   **결과**: `dp_table[-1][-1]` (테이블의 가장 마지막 값)이 모든 조건을 전체 문자열로 만족시키는 총 방법의 수가 됩니다.

3.  **결과 집계**:
    *   펼쳐진 모든 입력에 대해 `cal_case_num`을 호출하고 그 결과를 합산합니다.

이 DP 접근 방식은 부분 문제의 결과를 저장하고 재사용하여 중복 계산을 피함으로써 Part 1의 브루트포스 방식보다 훨씬 효율적으로 문제를 해결합니다.
