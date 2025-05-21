# 2023년 Day 4 Advent of Code 문제 풀이

## Part 1

### 문제 설명

Part 1에서는 스크래치 카드 세트가 주어집니다. 각 카드는 두 부분으로 나뉘어 있습니다: 하나는 당첨 번호 목록이고, 다른 하나는 가지고 있는 번호 목록입니다. 각 카드에 대해 점수를 계산해야 합니다. 점수 계산 규칙은 다음과 같습니다:
가지고 있는 번호 중 당첨 번호와 일치하는 번호의 개수를 `m`이라고 할 때,
*   `m = 0` (일치하는 번호 없음): 0점
*   `m > 0`: `2^(m-1)`점 (예: 1개 일치 시 1점, 2개 일치 시 2점, 3개 일치 시 4점 등)

모든 카드의 점수를 합산한 총 점수를 찾는 것이 목표입니다.

### 풀이 방법 (`part_1.py`)

1.  **입력 데이터 파싱 (`cal_num` 함수 내)**:
    *   각 카드 문자열 (예: "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")을 처리합니다.
    *   "Card X: " 부분을 제거하고, " | "를 기준으로 당첨 번호 부분과 가진 번호 부분을 분리합니다.
    *   각 부분을 공백 기준으로 나누어 숫자 리스트로 변환합니다.
    *   결과적으로 각 카드는 `[[당첨_번호_리스트], [가진_번호_리스트]]` 형태의 중첩 리스트로 표현됩니다.

2.  **카드 점수 계산 (`match_card` 함수)**:
    *   단일 카드 `[[당첨_번호_리스트], [가진_번호_리스트]]`를 입력으로 받습니다.
    *   효율적인 비교를 위해 당첨 번호 리스트와 가진 번호 리스트를 각각 파이썬 `set`으로 변환합니다.
    *   두 `set`의 교집합 (`&` 연산자 사용)을 구하여 일치하는 번호들의 `set`을 찾습니다.
    *   교집합의 크기 (`len()`)가 일치하는 번호의 개수 `m`이 됩니다.
    *   점수는 `int(2 ** (m - 1))`로 계산됩니다. `m`이 0이면 `2**(-1)`은 0.5가 되고, `int(0.5)`는 0이 되어 규칙에 맞게 처리됩니다.

3.  **총점 합산 (`cal_num` 함수 내)**:
    *   파싱된 모든 카드에 대해 `match_card` 함수를 호출하여 각 카드의 점수를 계산하고, 이 점수들을 모두 합산하여 최종 결과를 반환합니다.

## Part 2

### 문제 설명

Part 2에서는 Part 1과 동일한 스크래치 카드를 사용하지만, 점수 계산 방식 대신 카드 복사 규칙이 적용됩니다.
*   각 카드에서 일치하는 번호의 개수 `m`을 찾습니다.
*   카드 `X`에 `m`개의 일치하는 번호가 있다면, 카드 `X+1`, `X+2`, ..., `X+m`의 복사본을 각각 하나씩 얻게 됩니다.
*   이 규칙은 원본 카드뿐만 아니라 복사본 카드에도 동일하게 적용됩니다. 예를 들어, 카드 1의 복사본으로 카드 2를 얻었다면, 이 카드 2도 자체의 일치 규칙에 따라 추가 카드를 생성할 수 있습니다.

최종적으로 가지게 되는 모든 스크래치 카드(원본 + 복사본)의 총 개수를 계산하는 것이 목표입니다.

### 풀이 방법 (`part_2.py`)

1.  **입력 데이터 파싱 (`cal_num` 함수 내)**:
    *   Part 1과 동일하게 각 카드를 파싱하여 `[[당첨_번호_리스트], [가진_번호_리스트]]` 형태로 만듭니다.

2.  **일치하는 번호 개수 계산 (`match_card` 함수 - Part 2 버전)**:
    *   Part 1의 `match_card` 함수와 유사하지만, 점수 대신 **일치하는 번호의 개수** `m`을 직접 반환합니다.
    *   `len(winning_num_set & my_num_set)`을 반환합니다.

3.  **카드 복사 및 총 개수 계산 (`duplicate_card` 함수)**:
    *   `matched_score` 리스트를 입력으로 받습니다. 이 리스트는 각 원본 카드별 일치하는 번호의 개수를 담고 있습니다 (예: `matched_score[i]`는 `i+1`번 카드의 일치 개수).
    *   `card_num_list` 리스트를 생성하고 모든 값을 `1`로 초기화합니다. `card_num_list[i]`는 `i+1`번 카드의 총 보유 개수(원본 1개로 시작)를 나타냅니다.
    *   원본 카드를 순서대로 (`i`는 0부터 `총 원본 카드 수 - 1`까지) 반복합니다:
        *   `card_num = card_num_list[i]`: 현재 처리 중인 `i`번 카드의 총 보유 개수입니다.
        *   `matches_for_current_card = matched_score[i]`: `i`번 카드의 일치 번호 개수입니다.
        *   `i`번 카드의 각 사본(총 `card_num`개)에 대해, 다음 `matches_for_current_card`개의 카드의 사본을 얻습니다.
        *   따라서, `j`를 `1`부터 `matches_for_current_card`까지 반복하면서, `card_num_list[i + j]` (즉, `i+j`번 카드의 총 개수)에 `card_num`을 더합니다.
    *   모든 카드 처리가 끝난 후, `card_num_list`의 모든 요소를 합산하여 최종적으로 보유한 총 카드 수를 반환합니다.

4.  **실행 흐름 (`cal_num` 함수 내)**:
    *   먼저 모든 원본 카드에 대해 `match_card` (Part 2 버전)를 호출하여 각 카드별 일치 개수를 `matched_score` 리스트에 저장합니다.
    *   이 `matched_score` 리스트를 `duplicate_card` 함수에 전달하여 최종 카드 총 개수를 계산하고 반환합니다.The `README.md` file for `2023/day_4/` did not exist.
I have read and understood the logic for `part_1.py` and `part_2.py`.
- `part_1.py` calculates points for scratchcards based on matching numbers (`2^(matches-1)`).
- `part_2.py` calculates the total number of scratchcards (originals + copies) won, where matches on a card earn copies of subsequent cards.

I have now created the `2023/day_4/README.md` file with detailed explanations of both solutions in Korean, including problem descriptions, algorithmic approaches, and markdown formatting.
