# 2024년 Day 4 Advent of Code 문제 풀이

## Part 1

### 문제 설명

Part 1의 목표는 주어진 문자 그리드 내에서 "XMAS"라는 문자열이 나타나는 총 횟수를 찾는 것입니다. 검색은 다음 방향으로 수행되며, 겹치는 경우도 모두 계산에 포함됩니다:

1.  **수평**: 왼쪽에서 오른쪽으로, 그리고 오른쪽에서 왼쪽으로.
2.  **수직**: 위에서 아래로, 그리고 아래에서 위로.
3.  **대각선**:
    *   좌상단에서 우하단 방향 (및 그 반대 방향인 우하단에서 좌상단).
    *   우상단에서 좌하단 방향 (및 그 반대 방향인 좌하단에서 우상단).

### 풀이 방법 (`part_1.py`)

1.  **`count_overlapping_occurrences(string, substring)` 함수**:
    *   정규 표현식 `re.findall(f"(?={substring})", string)`을 사용하여 주어진 `string` 내에서 `substring`이 겹쳐서 나타나는 횟수를 계산합니다. `(?=...)`는 전방 탐색(lookahead assertion)으로, 문자열을 소비하지 않고 매칭되는 부분을 찾기 때문에 겹치는 부분을 계산할 수 있습니다.

2.  **`get_diagonals(input_data)` 함수**:
    *   입력 그리드 `input_data` (문자열 리스트)로부터 두 종류의 대각선 문자열들을 추출합니다.
    *   **좌상단-우하단 대각선 (`down_diagonals`)**:
        *   각 행의 앞쪽에 공백을 추가하여 (`add_front_padding`) 문자들을 정렬합니다. 예를 들어, 첫 번째 행은 공백 없이, 두 번째 행은 앞에 공백 1개, 세 번째 행은 공백 2개 등으로 패딩합니다.
        *   패딩된 그리드를 `zip(*add_front_padding)`을 사용하여 전치(transpose)합니다.
        *   전치된 결과의 각 열(원래 대각선에 해당)의 문자들을 합쳐 대각선 문자열을 만들고, 양 끝의 공백을 제거합니다.
    *   **우상단-좌하단 대각선 (`up_diagonals`)**:
        *   유사하게, 각 행의 뒤쪽에 공백을 추가하여 (`add_back_padding`) 다른 방향의 대각선을 추출합니다. (실제 코드에서는 `add_back_padding`이 `add_front_padding`과 동일한 로직으로 우하단-좌상단 대각선을 추출하게 되며, 전치 후 처리 방식이 다를 수 있으나, 일반적인 두 주요 대각선 방향을 의미합니다. 코드의 패딩 방식을 보면, `add_front_padding`은 좌상-우하 계열을, `add_back_padding`은 우상-좌하 계열을 추출하기 위한 정렬을 수행합니다.)
        *   정확히는, `add_front_padding`은 `i`개의 공백을 앞에, `add_back_padding`은 `len(line)-i-1`개의 공백을 앞에 추가하여 정렬합니다. `zip`으로 묶으면 각각 다른 대각선 세트가 나옵니다.
    *   추출된 두 종류의 대각선 문자열 튜플을 반환합니다.

3.  **`solution(input_data)` 함수**:
    *   `horizontals`: 원본 입력 데이터(행).
    *   `verticals`: `zip(*input_data)`를 사용하여 그리드를 전치하고 각 열을 합쳐 수직 문자열들을 생성합니다.
    *   `down_diagonals`, `up_diagonals`: `get_diagonals` 함수를 호출하여 대각선 문자열들을 가져옵니다.
    *   `checked_strings` 튜플에 이 네 가지 방향의 문자열 컬렉션(수평, 수직, 두 종류의 대각선)을 모두 저장합니다.
    *   `result`를 0으로 초기화합니다.
    *   `checked_strings`의 각 문자열 컬렉션(예: 모든 수평 문자열)에 대해 반복하고, 그 안의 각 개별 `string`에 대해 반복합니다:
        *   `result += count_overlapping_occurrences(string, "XMAS")`를 호출하여 "XMAS"의 등장 횟수를 더합니다.
        *   `result += count_overlapping_occurrences(string[::-1], "XMAS")`를 호출하여 뒤집힌 문자열에서도 "XMAS"의 등장 횟수를 더합니다 (예: "SAMX"를 찾기 위함).
    *   최종 `result`를 반환합니다.

## Part 2

### 문제 설명

Part 2에서는 주어진 문자 그리드에서 특정 3x3 "XMAS" 패턴의 총 등장 횟수를 찾는 것이 목표입니다. "XMAS" 패턴은 다음 조건을 만족해야 합니다:

1.  3x3 블록의 중앙 문자는 'A'여야 합니다.
2.  3x3 블록의 네 모서리 문자들(좌상단, 우상단, 좌하단, 우하단)은 정확히 두 개의 'M'과 두 개의 'S'로 구성되어야 합니다. 코드는 이 네 모서리 문자를 특정 순서(좌상단, 우상단, 좌하단, 우하단)로 연결했을 때 "MMSS", "SSMM", "MSMS", "SMSM" 중 하나와 일치하는지 확인합니다.

### 풀이 방법 (`part_2.py`)

1.  **`is_xmas(block)` 함수**:
    *   `block`은 3x3 크기의 문자 그리드 부분(세 개의 문자열로 구성된 튜플)을 입력으로 받습니다.
    *   `center_char = block[1][1]`: 3x3 블록의 중앙 문자를 가져옵니다.
    *   `angle_chars = block[0][0] + block[0][2] + block[2][0] + block[2][2]`: 네 모서리 문자(좌상단, 우상단, 좌하단, 우하단 순서)를 순서대로 연결하여 문자열을 만듭니다.
    *   `valid_angle_chars = {"MMSS", "SSMM", "MSMS", "SMSM"}`: 유효한 모서리 문자 패턴들의 집합입니다.
    *   중앙 문자가 'A'이고, `angle_chars` 문자열이 `valid_angle_chars` 집합 내에 있으면 `True` (즉, 1)를 반환하고, 그렇지 않으면 `False` (즉, 0)를 반환합니다.

2.  **`solution(input_data)` 함수**:
    *   `result`를 0으로 초기화합니다.
    *   입력 그리드 `input_data`를 순회하며 가능한 모든 3x3 블록의 중앙 위치 `(i, j)`를 찾습니다. (경계를 고려하여 `i`는 `1`부터 `len(input_data) - 2`까지, `j`는 `1`부터 `len(input_data[i]) - 2`까지 반복).
    *   각 중앙 위치 `(i, j)`에 대해, 해당 위치를 중심으로 하는 3x3 블록 `block`을 추출합니다.
        *   `block = (input_data[i-1][j-1:j+2], input_data[i][j-1:j+2], input_data[i+1][j-1:j+2])`
    *   추출된 `block`에 대해 `is_xmas(block)` 함수를 호출하고, 그 결과를 `result`에 더합니다.
    *   모든 가능한 3x3 블록을 확인한 후 최종 `result`를 반환합니다.