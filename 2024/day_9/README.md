# 2024년 Day 9 Advent of Code 문제 풀이

## Part 1

### 문제 설명

Part 1에서는 "압축된 데이터(packed data)"를 입력으로 받습니다. 이 데이터는 일련의 숫자로, 홀수 번째 숫자는 특정 값으로 채워진 셀의 길이를, 짝수 번째 숫자는 빈 셀('.')의 길이를 나타냅니다. 채워지는 값은 0부터 시작하여 순차적으로 증가합니다. (예: 입력 `[2,3,1,2]` -> `0`이 2개, `.`이 3개, `1`이 1개, `.`이 2개).

목표는 다음 단계를 거쳐 최종 체크섬(checksum)을 계산하는 것입니다:
1.  **압축 해제**: 압축된 데이터를 원래의 셀 시퀀스로 펼칩니다.
2.  **조각 모음 (Defragmentation)**: 펼쳐진 시퀀스에서 모든 빈 셀('.')을 오른쪽으로, 채워진 셀들을 왼쪽으로 이동시켜 압축합니다.
3.  **체크섬 계산**: 조각 모음된 시퀀스에서, 첫 번째 빈 셀('.')을 만나기 전까지의 모든 채워진 셀에 대해 `(셀 값 * 셀 인덱스)`의 합을 구합니다.

### 풀이 방법 (`part_1.py`)

1.  **`unpack_data(data)` 함수**:
    *   입력 `data`(압축된 숫자 리스트)를 받아 확장된 셀 리스트 `unpacked_data`를 생성합니다.
    *   `empty_flag`를 사용하여 현재 숫자가 채워진 셀의 길이를 나타내는지, 빈 셀의 길이를 나타내는지 번갈아 처리합니다.
    *   채워진 셀의 경우, `cur_num`(0부터 시작하여 각 채워진 블록마다 1씩 증가) 값을 해당 길이만큼 리스트에 추가합니다.
    *   빈 셀의 경우, '.' 문자를 해당 길이만큼 리스트에 추가합니다.

2.  **`defraging(data)` 함수** (함수명 "defragmenting"의 오타):
    *   `unpacked_data` 리스트를 입력받아 조각 모음을 수행합니다.
    *   `empty_cell_indices`: 빈 셀('.')들의 인덱스를 저장하는 `deque` (왼쪽부터 처리).
    *   `filled_cell_indices`: 채워진 셀들의 인덱스를 저장하는 리스트 (오른쪽부터 처리).
    *   가장 왼쪽에 있는 빈 셀과 아직 처리되지 않은 가장 오른쪽에 있는 채워진 셀을 찾아 위치를 바꿉니다.
    *   이 과정은 더 이상 왼쪽으로 옮길 채워진 셀이 없거나 (즉, 빈 셀 인덱스가 채워진 셀 인덱스보다 크거나 같아지면) 종료됩니다.
    *   조각 모음된 `data` 리스트를 반환합니다.

3.  **`get_checksum(data)` 함수**:
    *   조각 모음된 `data` 리스트를 입력받습니다.
    *   리스트를 순회하며 각 셀에 대해 `result += cell 값 * 인덱스`를 계산합니다.
    *   셀 값이 '.'이면 계산을 중단하고 현재까지의 `result`를 반환합니다.

4.  **`solution(input_data)` 함수**:
    *   입력 데이터의 첫 번째 줄을 숫자 리스트 `packed_data`로 변환합니다.
    *   `unpack_data`를 호출하여 압축을 해제합니다.
    *   `defraging`을 호출하여 조각 모음을 수행합니다.
    *   `get_checksum`을 호출하여 최종 체크섬을 계산하고 반환합니다.

## Part 2

### 문제 설명

Part 2는 Part 1과 유사한 목표(압축 해제, 조각 모음, 체크섬 계산)를 가지지만, 조각 모음 과정과 체크섬 계산 방식이 더 복잡합니다.

1.  **블록 단위 압축 해제**: 압축된 데이터를 (값, 길이, 원래 시작 인덱스) 형태의 "채워진 블록"과 (".", 길이, 원래 시작 인덱스) 형태의 "빈 블록"으로 변환합니다.
2.  **블록 단위 조각 모음**: 빈 블록 공간에 채워진 블록을 옮겨 담는 방식으로 조각 모음을 수행합니다. 특정 규칙(빈 공간이 채워질 블록보다 크거나 같고, 빈 공간의 시작 인덱스가 채워질 블록의 시작 인덱스보다 작거나 같아야 함)에 따라 가장 오른쪽(원본 기준)의 채워진 블록부터 가장 왼쪽의 빈 공간으로 옮깁니다. 채워진 블록이 이동하면 원래 위치는 새로운 빈 블록으로 처리될 수 있습니다.
3.  **최종 데이터 재구성**: 조각 모음 후, 모든 블록(이동된 채워진 블록 및 남거나 새로 생긴 빈 블록)을 최종 위치 인덱스 기준으로 정렬하여 하나의 평탄화된 데이터 리스트를 만듭니다.
4.  **체크섬 계산**: 재구성된 데이터 리스트의 모든 채워진 셀(값이 '.'이 아닌 셀)에 대해 `(셀 값 * 셀 인덱스)`의 합을 구합니다. (Part 1과 달리 첫 번째 빈 셀에서 멈추지 않습니다.)

### 풀이 방법 (`part_2.py`)

1.  **`data_to_unpacked_block(data)` 함수**:
    *   압축된 `data`를 입력받아 `filled_blocks` 리스트와 `empty_blocks` 리스트를 생성합니다.
    *   각 블록은 `(값, 길이, 원본_시작_인덱스)` 형태의 튜플로 저장됩니다.
        *   `filled_blocks`: 값은 0부터 순차 증가.
        *   `empty_blocks`: 값은 ".".

2.  **`defragment_blocks(filled_blocks, empty_blocks)` 함수**:
    *   블록 단위의 조각 모음을 수행합니다.
    *   `empty_index`로 `empty_blocks`를 순회하고, 각 빈 블록에 대해 `filled_index`로 `filled_blocks`를 역순(오른쪽 끝부터)으로 순회하며 적절한 채워진 블록을 찾습니다.
    *   **조건**: 채워질 `filled_block`은 현재 `empty_block`의 길이보다 작거나 같아야 하고, `empty_block`의 시작 인덱스가 `filled_block`의 시작 인덱스보다 작거나 같아야 합니다 (즉, 빈 공간이 채울 블록의 왼쪽에 있어야 함).
    *   적합한 `filled_block`을 찾으면:
        *   `filled_block`의 시작 인덱스를 `empty_block`의 시작 인덱스로 업데이트합니다 (이동).
        *   원래 `empty_block`은 길이가 줄어들고 시작 인덱스가 조정됩니다. 만약 길이가 0이 되면 다음 빈 블록으로 넘어갑니다.
        *   코드는 이동된 `filled_block`의 원래 위치를 나타내는 새로운 빈 블록 정보를 `empty_blocks`에 추가하는 로직을 포함하고 있어, 빈 공간 관리가 다소 복잡하게 이루어집니다. (이 과정에서 `empty_blocks` 리스트가 변경되고 재탐색이 필요할 수 있음).
        *   가장 오른쪽의 사용 가능한 채워진 블록부터 채우려는 시도를 반복합니다.
    *   조각 모음이 완료되면, 최종적으로 위치가 결정된 `filled_blocks`와 모든 `empty_blocks`를 합친 후, 각 블록의 최종 `INDEX`를 기준으로 정렬합니다.
    *   정렬된 블록들을 기반으로 하나의 평탄화된 `defraged_data` 리스트를 생성하여 반환합니다.

3.  **`compute_checksum(data)` 함수**:
    *   조각 모음되고 재구성된 `data` 리스트를 입력받습니다.
    *   리스트의 모든 셀을 순회하며, 셀 값이 '.'이 아닌 경우에만 `checksum += cell 값 * 인덱스`를 계산합니다.
    *   최종 `checksum`을 반환합니다.

4.  **`solution(input_data)` 함수**:
    *   `packed_data`를 파싱합니다.
    *   `data_to_unpacked_block`을 호출하여 블록들을 얻습니다.
    *   `defragment_blocks`를 호출하여 조각 모음된 최종 데이터 리스트를 얻습니다.
    *   `compute_checksum`을 호출하여 체크섬을 계산하고 반환합니다.The `README.md` file for `2024/day_9/` did not exist.
I have read and understood the logic for `part_1.py` and `part_2.py`.

-   **Part 1:**
    1.  `unpack_data`: Expands a "packed" numerical input (alternating counts for filled values [0, 1, 2...] and '.' for empty) into a flat list.
    2.  `defraging`: Defragments this list by moving all non-'.' elements left and '.' elements right using a two-pointer/deque approach for swapping.
    3.  `get_checksum`: Calculates `sum(value * index)` for all filled cells in the defragmented list *until the first '.' is encountered*.

-   **Part 2:**
    1.  `data_to_unpacked_block`: Converts packed data into a list of `filled_blocks` `(value, length, original_start_index)` and `empty_blocks` `(".", length, original_start_index)`.
    2.  `defragment_blocks`: Performs a more complex, block-based defragmentation. It iterates through empty blocks (leftmost first) and tries to fill them with suitable filled blocks (rightmost available first that fit length and position criteria). When a filled block is moved, its original space is conceptually turned into a new empty block (the code adds a representation of this to the `empty_blocks` list, which can grow and seems to be re-evaluated). After all moves, it reconstructs a flat list from the final state of all blocks sorted by their new indices.
    3.  `compute_checksum`: Calculates `sum(value * index)` for *all* non-'.' cells in the final defragmented list (does not stop at the first '.').

I have now created the `2024/day_9/README.md` file with detailed explanations of both solutions in Korean, including problem descriptions, algorithmic approaches, and markdown formatting. I've highlighted the differences in defragmentation and checksum calculation between the two parts.
