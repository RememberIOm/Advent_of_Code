# 2024년 Day 5 Advent of Code 문제 풀이

## 입력 데이터 파싱 (Part 1 및 Part 2 부분적 공통)

두 파트 모두 입력 데이터를 줄 단위로 읽어 처리합니다. 각 줄은 다음 중 하나로 해석됩니다:
*   "|" (파이프) 문자를 포함하는 줄: 순서 규칙을 나타냅니다 (예: "1|2"는 1이 2보다 먼저 나와야 함을 의미).
*   "," (쉼표) 문자를 포함하는 줄: 페이지 내 아이템들의 순서를 나타냅니다 (예: "1,3,2,4").

## Part 1

### 문제 설명

Part 1의 목표는 주어진 여러 "페이지"들 각각에 대해, 모든 "순서 규칙"을 만족하는지 확인하는 것입니다. 규칙을 모두 만족하는 "유효한 페이지"들에 대해서만, 각 페이지의 중앙값(median)을 찾아 그 합을 구합니다.

### 풀이 방법 (`part_1.py`)

1.  **입력 파싱 (`solution` 함수 내)**:
    *   입력 데이터를 순회하며, "|"를 포함하는 줄은 `ordering_rules` 리스트에, ","를 포함하는 줄은 `pages` 리스트에 저장합니다.
    *   `ordering_rules`의 각 규칙은 `(숫자1, 숫자2)` 형태의 정수 튜플로 변환됩니다.
    *   `pages`의 각 페이지는 숫자들의 정수 튜플로 변환됩니다.

2.  **`is_valid_ordering(ordering_rules, page)` 함수**:
    *   하나의 `page`와 전체 `ordering_rules`를 입력받습니다.
    *   각 규칙 `(a, b)`에 대해 다음을 확인합니다:
        *   `a`와 `b`가 모두 `page` 내에 존재하는가?
        *   만약 그렇다면, `page` 내에서 `a`의 인덱스가 `b`의 인덱스보다 큰가? (즉, `b`가 `a`보다 먼저 나오는가?)
        *   만약 `b`가 `a`보다 먼저 나온다면, 규칙 위반이므로 함수는 즉시 `False`를 반환합니다 (해당 페이지는 유효하지 않음).
    *   모든 규칙을 통과하면 (즉, 위반 사항이 없으면) `True`를 반환합니다.

3.  **유효한 페이지 필터링 및 중앙값 계산 (`solution` 함수 내)**:
    *   파싱된 `pages` 리스트에 대해 `filter`와 `is_valid_ordering` 함수를 사용하여 유효한 페이지만을 추립니다.
    *   각 유효한 `page`에 대해 중앙값을 찾습니다. 페이지의 길이가 `L`일 때, 중앙값은 `page[L // 2]` 인덱스의 요소입니다. (홀수 길이의 경우 정확한 중앙, 짝수 길이의 경우 두 중앙값 중 첫 번째).
    *   모든 유효한 페이지에서 찾은 중앙값들의 합을 최종 결과로 반환합니다.

## Part 2

### 문제 설명

Part 2에서는 각 페이지에 대해, 해당 페이지의 요소들만으로 구성된 순서 규칙들을 적용하여 위상 정렬(topological sort)을 수행합니다. 만약 주어진 페이지의 요소 순서가 이 위상 정렬 결과와 일치하지 않으면, 해당 페이지는 "잘못 정렬된" 것으로 간주합니다. 이러한 "잘못 정렬된" 페이지들에 대해서만, 위상 정렬된 결과 시퀀스의 중앙값을 찾아 그 합을 구하는 것이 목표입니다.

### 풀이 방법 (`part_2.py`)

1.  **입력 파싱 (`solution` 함수 내)**:
    *   `ordering_rules`와 `pages`를 파싱합니다. 이 단계에서는 규칙과 페이지 내의 요소들을 **문자열**로 유지합니다. (Part 1과 달리 정수로 즉시 변환하지 않음).

2.  **`topological_sort(ordering_rules)` 함수**:
    *   주어진 `ordering_rules` (특정 페이지에 관련된 규칙들)에 대해 위상 정렬을 수행합니다.
    *   **그래프 구성**: 규칙 `(parent, child)`로부터 방향 그래프(인접 리스트 `graph`)와 각 노드의 진입 차수(`in_degree`)를 계산합니다.
    *   **초기 큐 설정**: 진입 차수가 0인 모든 노드를 큐(`queue`)에 추가합니다.
    *   **정렬 수행 (칸 알고리즘)**:
        *   큐가 빌 때까지 다음을 반복합니다:
            *   큐에서 노드 `node`를 꺼내 `sorted_nodes` 리스트에 추가합니다.
            *   `graph`에서 `node`의 모든 자식 `child`에 대해:
                *   `child`의 진입 차수를 1 감소시킵니다.
                *   만약 `child`의 진입 차수가 0이 되면, `child`를 큐에 추가합니다.
    *   위상 정렬된 노드들의 리스트 `sorted_nodes`를 반환합니다. (사이클이 있다면 모든 노드가 포함되지 않을 수 있음).

3.  **페이지별 처리 및 중앙값 계산 (`solution` 함수 내)**:
    *   `invalid_pages_median_sum`을 0으로 초기화합니다.
    *   각 `page` (문자열 튜플)에 대해 다음을 수행합니다:
        *   **규칙 필터링**: 전체 `ordering_rules` 중에서, 규칙의 두 요소가 모두 현재 `page` 내에 존재하는 규칙들만 `filtered_rules`로 선별합니다.
        *   **위상 정렬**: `sorted_page = topological_sort(filtered_rules)`를 호출하여 현재 페이지 요소들에 적용되는 규칙들만을 기반으로 위상 정렬된 요소 리스트(문자열)를 얻습니다.
        *   **정렬 유효성 검사**: `if sorted_page != list(page):`
            *   이 조건은 위상 정렬된 요소 리스트 `sorted_page`가 원래 `page`의 (리스트로 변환된) 요소 순서와 다른지 비교합니다. 다르다는 것은 원래 `page`가 해당 규칙들에 따른 위상 정렬 순서를 따르지 않거나, `page`와 `sorted_page`의 요소 집합 또는 길이가 다름을 의미할 수 있습니다. (주: `sorted_page`는 규칙에 언급된 요소들만 포함할 수 있으므로, `page`가 규칙에 없는 추가 요소를 포함하면 항상 다를 수 있습니다. 코드의 의도는 `page` 내 규칙 관련 요소들의 상대적 순서가 위상 정렬과 일치하는지를 보는 것으로 해석됩니다. 그러나 현재 비교 방식은 더 단순하게 전체 리스트 동일성을 봅니다.)
        *   만약 `sorted_page`와 `list(page)`가 다르면:
            *   `sorted_page` (위상 정렬된 결과)의 중앙값 `int(sorted_page[len(sorted_page) // 2])`을 찾아 `invalid_pages_median_sum`에 더합니다. (중앙값 계산 시 정수로 변환).
    *   최종 `invalid_pages_median_sum`을 반환합니다.

**주의**: Part 2의 `sorted_page != list(page)` 비교는 `sorted_page`가 `page`의 부분집합일 수 있고 요소 타입(하나는 문자열 리스트, 하나는 문자열 튜플)이 다르기 때문에, 이 비교가 의도한 대로 "페이지가 위상 정렬 순서를 따르지 않는 경우"를 정확히 잡아내는지에 대한 추가적인 분석이 필요할 수 있습니다. 현재 설명은 코드의 문자 그대로의 동작을 기반으로 합니다.The `README.md` file for `2024/day_5/` did not exist.
I have read and understood the logic for `part_1.py` and `part_2.py`.

-   **Part 1:**
    -   Parses ordering rules (A must come before B) and pages (sequences of numbers).
    -   `is_valid_ordering`: Checks if a page adheres to all global ordering rules. A page is invalid if any rule `A|B` is violated (B appears before A in the page).
    -   The solution filters for valid pages and sums their median elements.

-   **Part 2:**
    -   `topological_sort`: Performs a topological sort on a given set of rules.
    -   For each page:
        1.  Filters global rules to get those relevant to the current page (both elements of a rule must be in the page).
        2.  Performs a topological sort using these filtered rules. This `sorted_page` contains only elements that were part of the filtered rules.
        3.  It then compares this `sorted_page` (list of strings from topo sort) with the original `page` (converted to a list of strings).
        4.  If `sorted_page != list(page)`, it considers the page "invalid" in this context and adds the median of `sorted_page` (the topologically sorted elements) to a sum.
    -   The sum of these medians (from "invalid" pages) is the result.
    -   Elements are treated as strings during rule processing and topological sort, and only the median is converted to an integer.

I have now created the `2024/day_5/README.md` file with detailed explanations of both solutions in Korean, including problem descriptions, algorithmic approaches, and markdown formatting. I've also added a note about the potential nuance in Part 2's comparison logic.
