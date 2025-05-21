# 2024년 Day 7 Advent of Code 문제 풀이

## 공통 입력 파싱 로직

Part 1과 Part 2의 `solution` 함수는 유사한 초기 입력 파싱 로직을 공유합니다:

1.  입력 데이터 (`input_data`)는 각 줄이 "LHS: RHS_숫자1 RHS_숫자2 ..." 형태의 문자열로 구성된 리스트입니다.
    (예: "100: 5 5 5" 또는 "75: 3 5 3")
2.  각 줄은 콜론(":")을 기준으로 왼쪽 부분(LHS)과 오른쪽 부분(RHS)으로 분리됩니다.
3.  LHS는 정수로 변환됩니다.
4.  RHS는 공백을 기준으로 분리된 후, 각 숫자가 정수로 변환되어 숫자 리스트가 됩니다.
5.  파싱된 각 방정식은 `(LHS_정수, RHS_숫자리스트)` 형태의 튜플로 `equations` 리스트에 저장됩니다.

## Part 1

### 문제 설명

Part 1의 목표는 주어진 각 방정식에 대해, RHS 숫자들 사이에 '+'(덧셈) 또는 '*'(곱셈) 연산자를 삽입하여 LHS 값과 동일한 결과를 만들 수 있는지 확인하는 것입니다. 연산은 왼쪽에서 오른쪽 순서로 엄격하게 적용되며, 일반적인 연산자 우선순위(예: 곱셈이 덧셈보다 먼저)는 적용되지 않습니다.

만약 RHS 숫자들 사이에 연산자를 적절히 배치하여 LHS 값과 같은 결과를 얻을 수 있는 방정식이 있다면, 해당 방정식의 LHS 값을 합산합니다. 모든 "풀 수 있는" 방정식들의 LHS 값의 총합을 구하는 것이 최종 목표입니다.

### 풀이 방법 (`part_1.py`)

1.  **`check_equtaion(equation)` 함수** (코드 내 함수명에 오타 "equtaion"이 있으나, 기능 설명은 정확한 철자 "equation"을 기준으로 함):
    *   하나의 `equation` 튜플 `(left, right_nums_list)`을 입력으로 받습니다.
    *   `itertools.product("+*", repeat=len(right_nums_list) - 1)`를 사용하여 RHS 숫자들 사이에 배치할 수 있는 모든 가능한 연산자 ('+' 또는 '*') 조합을 생성합니다. `right_nums_list`에 `N`개의 숫자가 있다면, `N-1`개의 연산자 슬롯이 있습니다.
    *   생성된 각 연산자 조합(`operators`)에 대해 다음을 수행합니다:
        *   `result` 변수를 `right_nums_list[0]` (RHS의 첫 번째 숫자)으로 초기화합니다.
        *   `right_nums_list`의 나머지 숫자들과 해당 위치의 `operator`를 순서대로 가져와 연산을 적용합니다:
            *   `operator`가 '+'이면 `result += num`.
            *   `operator`가 '*'이면 `result *= num`.
        *   모든 연산을 적용한 후, 최종 `result`가 LHS 값 `left`와 같다면, 해당 방정식은 풀 수 있는 것으로 간주하고 즉시 `True`를 반환합니다.
    *   모든 연산자 조합을 시도해도 `result == left`가 되는 경우가 없다면, `False`를 반환합니다.

2.  **`solution(input_data)` 함수**:
    *   위에 설명된 대로 모든 입력 줄을 파싱하여 `equations` 리스트를 생성합니다.
    *   `filter(check_equtaion, equations)`를 사용하여 `check_equtaion` 함수가 `True`를 반환하는 방정식들만 필터링합니다.
    *   필터링된 "풀 수 있는" 방정식들의 LHS 값 (`eq[0]`)들을 모두 합산하여 최종 결과를 반환합니다.

## Part 2

### 문제 설명

Part 2는 Part 1과 유사하지만, 사용할 수 있는 연산자에 '|'(이어붙이기)가 추가됩니다.
*   '+' (덧셈)
*   '*' (곱셈)
*   '|' (이어붙이기): 두 숫자 A와 B에 대해 `A | B`는 `int(str(A) + str(B))`로 계산됩니다. 예를 들어, `12 | 3`은 `123`이 됩니다.

연산은 여전히 왼쪽에서 오른쪽 순서로 엄격하게 적용됩니다. RHS 숫자들 사이에 '+', '*', '|' 연산자를 적절히 삽입하여 LHS 값과 동일한 결과를 만들 수 있는 방정식들의 LHS 값의 총합을 구하는 것이 목표입니다.

### 풀이 방법 (`part_2.py`)

1.  **`check_equtaion(equation)` 함수** (코드 내 함수명 오타 동일):
    *   Part 1의 `check_equtaion` 함수와 매우 유사합니다.
    *   주요 차이점은 연산자 조합을 생성할 때 `itertools.product("+*|", repeat=len(right_nums_list) - 1)`를 사용하여 '|' 연산자도 포함시킨다는 것입니다.
    *   연산을 적용하는 부분에 '|' 연산자에 대한 처리가 추가됩니다:
        *   `operator`가 '|'이면 `result = int(str(result) + str(num))`.
    *   나머지 로직(결과 비교 및 반환)은 Part 1과 동일합니다.

2.  **`solution(input_data)` 함수**:
    *   Part 1의 `solution` 함수와 동일합니다. 입력 파싱 후, Part 2 버전의 `check_equtaion` 함수를 사용하여 풀 수 있는 방정식을 필터링하고, 그 LHS 값들의 합을 반환합니다.

이 문제의 핵심은 `itertools.product`를 사용하여 가능한 모든 연산자 순열을 생성하고, 각 순열에 따라 RHS를 계산하여 LHS와 일치하는지 확인하는 완전 탐색(brute-force) 접근 방식입니다.