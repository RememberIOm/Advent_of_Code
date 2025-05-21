# 2023년 Day 5 Advent of Code 문제 풀이

## 입력 데이터 파싱 (Part 1 및 Part 2 공통)

두 파트 모두 유사한 방식으로 입력 데이터를 파싱합니다.

1.  **초기 시드(Seed) 추출**:
    *   입력의 첫 번째 줄 ("seeds: ...")에서 초기 시드 번호 목록을 추출합니다.
        *   Part 1에서는 이들이 개별 시드 번호입니다.
        *   Part 2에서는 이들이 `(시작_시드, 길이)` 쌍으로 해석되어 시드 범위를 나타냅니다.

2.  **매핑 레이어(Layer) 구성**:
    *   입력 데이터에서 "seed-to-soil map:", "soil-to-fertilizer map:" 등과 같은 섹션 헤더를 찾아 각 변환 단계(레이어)의 시작을 식별합니다.
    *   각 레이어는 여러 줄의 매핑 규칙으로 구성됩니다. 각 규칙은 `(목적지_시작_번호, 소스_시작_번호, 길이)` 형태의 세 숫자로 주어집니다.
    *   파싱 결과, `layers`는 이러한 매핑 규칙들의 리스트(각 레이어)를 요소로 가지는 리스트가 됩니다.

## Part 1

### 문제 설명

Part 1의 목표는 주어진 초기 시드 번호 목록을 여러 단계의 매핑 레이어를 통해 변환하여, 최종적으로 가장 낮은 "위치(location)" 번호를 찾는 것입니다. 각 매핑 레이어는 특정 종류의 값(예: 시드)을 다른 종류의 값(예: 토양)으로 변환하는 규칙들을 포함합니다.

*   한 레이어 내에서 특정 시드 번호는 여러 규칙 중 첫 번째로 일치하는 규칙에 의해서만 변환됩니다.
*   만약 시드 번호가 해당 레이어의 어떤 규칙의 소스 범위에도 해당하지 않으면, 그 시드 번호는 다음 레이어로 변경 없이 그대로 전달됩니다.

### 풀이 방법 (`part_1.py`)

1.  **`solution(input_data)` 함수**:
    *   입력 데이터를 파싱하여 초기 `seeds` 리스트와 `layers`를 구성합니다.
    *   `cal_seeds(seeds, layers)` 함수를 호출하여 모든 시드를 모든 레이어에 걸쳐 변환합니다.
    *   변환된 최종 시드 번호들 중 가장 작은 값을 반환합니다 (`min(seeds)`).

2.  **`cal_seeds(seeds, layers)` 함수**:
    *   모든 `layers`를 순차적으로 반복합니다.
    *   각 `layer`에 대해, 현재 `seeds` 리스트의 각 시드 번호를 `cal_seed(seed, layer)` 함수를 사용하여 변환하고, `seeds` 리스트를 업데이트합니다.

3.  **`cal_seed(seed, layer)` 함수**:
    *   단일 `seed` 번호와 하나의 `layer`(매핑 규칙들의 리스트)를 입력으로 받습니다.
    *   `layer` 내의 각 `layer_element`(규칙)에 대해 `is_include(seed, layer_element)`를 호출하여 `seed`가 해당 규칙의 소스 범위 (`소스_시작_번호` 부터 `소스_시작_번호 + 길이 - 1` 까지)에 포함되는지 확인합니다.
        *   **주의**: 코드 내 `is_include` 함수는 `소스_시작_번호 <= seed <= 소스_시작_번호 + 길이`로 검사하고 있어, 일반적인 길이 해석(개수)과는 약간 다를 수 있습니다. 이 설명은 코드의 동작을 기준으로 합니다.
    *   만약 `seed`가 규칙의 소스 범위에 포함되면, `seed`는 `seed + (목적지_시작_번호 - 소스_시작_번호)`로 변환되고, 이 변환된 값이 즉시 반환됩니다 (해당 레이어에서는 더 이상 다른 규칙을 확인하지 않음).
    *   `layer` 내의 어떤 규칙과도 일치하지 않으면, 원래 `seed` 값이 그대로 반환됩니다.

4.  **`is_include(seed, layer_element)` 함수**:
    *   `seed`가 `layer_element` 규칙의 소스 범위 (`layer_element[1]`부터 `layer_element[1] + layer_element[2]`까지)에 포함되는지 여부를 boolean 값으로 반환합니다.

## Part 2

### 문제 설명

Part 2는 Part 1과 유사하지만, 초기 시드가 개별 번호가 아닌 범위(`시작_번호`, `길이`)로 주어집니다. 이 많은 수의 시드를 개별적으로 처리하는 것은 비효율적이므로, 범위 자체를 변환해야 합니다. 목표는 모든 초기 시드 범위에서 시작하여 모든 매핑 단계를 거친 후 도달할 수 있는 가장 낮은 위치 번호를 찾는 것입니다.

### 풀이 방법 (`part_2.py`)

1.  **`solution(input_data)` 함수**:
    *   입력 데이터를 파싱합니다. 초기 `seeds`는 `[(시작_번호1, 길이1), (시작_번호2, 길이2), ...]` 형태의 범위 리스트로 변환됩니다. `layers` 구성은 Part 1과 동일합니다.
    *   `cal_seeds(seeds, layers)` 함수 (Part 2 버전)를 호출하여 시드 범위들을 모든 레이어에 걸쳐 변환합니다.
    *   변환된 최종 범위 리스트를 시작 번호 기준으로 정렬한 후, 가장 첫 번째 범위의 시작 번호 (`seeds[0][0]`)를 최소 위치로 반환합니다.

2.  **`cal_seeds(seeds, layers)` 함수 (Part 2 버전)**:
    *   모든 `layers`를 순차적으로 반복합니다.
    *   각 `layer`에 대해, 현재 `seeds` 범위 리스트를 `cal_range(seeds, layer)` 함수를 사용하여 변환하고, `seeds` 리스트를 업데이트합니다.

3.  **`cal_range(seeds, layer)` 함수**:
    *   현재 `seeds` 범위 리스트와 하나의 `layer`를 입력으로 받습니다.
    *   `processed_seeds` 리스트를 초기화하여 현재 `layer`에서 변환된 범위들을 저장합니다.
    *   입력된 각 `seed_range` (하나의 시드 범위 `(시작, 길이)`)에 대해 다음을 수행합니다:
        *   `unprocessed_seeds`를 현재 `seed_range`만 포함하는 리스트로 초기화합니다. 이 리스트는 현재 `layer`의 규칙들에 의해 아직 처리되지 않은 해당 `seed_range`의 부분들을 추적합니다.
        *   `layer` 내의 각 `layer_element`(매핑 규칙)를 순회합니다:
            *   `unprocessed_seeds` 내의 각 `current_unprocessed_part`에 대해 `cal_seed(current_unprocessed_part, layer_element)` (Part 2 버전의 범위 처리 함수)를 호출합니다.
            *   `cal_seed`는 `current_unprocessed_part`를 `layer_element` 규칙과 비교하여, 규칙에 의해 변환된 부분(`processed_parts_from_rule`)과 변환되지 않고 남은 부분(`still_unprocessed_parts`)으로 나눕니다.
            *   변환된 부분들은 최종 `processed_seeds` 리스트에 추가되고, 변환되지 않은 부분들은 다음 `layer_element` 규칙과 비교하기 위해 임시 리스트(`next_unprocessed_seeds`)에 저장됩니다.
            *   한 `layer_element` 처리가 끝나면, `unprocessed_seeds`는 `next_unprocessed_seeds`로 업데이트됩니다.
        *   한 `seed_range`에 대해 `layer` 내의 모든 규칙을 적용한 후에도 `unprocessed_seeds`에 남아있는 범위들은 어떤 규칙과도 매칭되지 않은 것이므로, 원본 그대로 최종 `processed_seeds`에 추가됩니다.
    *   모든 입력 `seed_range` 처리가 끝나면, 변환된 범위들의 새 리스트인 `processed_seeds`를 반환합니다.

4.  **`cal_seed(seed_range, layer_element)` 함수 (Part 2 버전 - 범위 처리)**:
    *   하나의 시드 범위 `seed_range = (시드_시작, 시드_길이)`와 하나의 매핑 규칙 `layer_element = (목적지_시작, 소스_시작, 규칙_길이)`를 입력으로 받습니다.
    *   `seed_range`와 `layer_element`의 소스 범위 간의 관계를 분석하여 겹치는 부분을 찾습니다.
    *   **완전히 포함**: `seed_range` 전체가 규칙의 소스 범위 내에 있으면, `seed_range` 전체가 변환되어 `processed_seed` 리스트에 추가됩니다.
    *   **완전히 미포함**: `seed_range`가 규칙의 소스 범위와 전혀 겹치지 않으면, `seed_range` 전체가 `unprocessed_seed` 리스트에 추가됩니다.
    *   **부분적으로 겹침**: `seed_range`는 최대 세 부분으로 나뉠 수 있습니다:
        *   규칙의 소스 범위 이전 부분 (겹치지 않음) -> `unprocessed_seed`에 추가.
        *   규칙의 소스 범위와 겹치는 부분 -> 변환되어 `processed_seed`에 추가.
        *   규칙의 소스 범위 이후 부분 (겹치지 않음) -> `unprocessed_seed`에 추가.
    *   변환된 범위들의 리스트 (`processed_seed`)와 이 규칙에 의해 변환되지 않은 부분들의 리스트 (`unprocessed_seed`)를 반환합니다.

이 범위 기반 처리 방식은 Part 2에서 발생할 수 있는 엄청난 수의 개별 시드를 효율적으로 다룰 수 있게 해줍니다.