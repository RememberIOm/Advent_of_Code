# 2024년 Day 3 Advent of Code 문제 풀이

## 개요

이 문제의 Day 3은 주어진 전체 텍스트 입력에서 특정 패턴의 문자열을 찾아 연산을 수행하는 과제입니다. Part 1은 "mul(숫자1,숫자2)" 형태의 모든 부분 문자열을 찾아 두 숫자의 곱을 합산하는 것이고, Part 2는 이 곱셈 연산이 특정 조건("do()" 또는 "don't()" 상태)에 따라 활성화될 때만 합산하는 것입니다. 각 파트에 대해 두 가지 접근 방식(수동 파싱과 정규 표현식 사용)의 솔루션 코드가 제공됩니다.

모든 솔루션에서 입력 데이터는 여러 줄로 주어질 수 있지만, 처리 시작 시 `"".join(input_data)`를 통해 단일 문자열로 합쳐집니다.

## Part 1

Part 1의 목표는 입력 문자열에서 "mul(숫자1,숫자2)" 형식의 모든 유효한 부분 문자열을 찾아, 각 경우에 대해 `숫자1 * 숫자2`를 계산하고 이들의 총합을 구하는 것입니다.

### Part 1 - 수동 파싱 방식 (`part_1_with_parse.py`)

1.  **`mul(string)` 함수**:
    *   "mul(a,b)" 형태의 문자열 `string`을 입력으로 받습니다.
    *   문자열 슬라이싱 (`string[4:-1]`)과 `split(',')`을 사용하여 숫자 부분 "a"와 "b"를 문자열 형태로 추출합니다.
    *   추출된 부분이 정확히 두 개이고, 두 부분 모두 숫자로만 구성되어 있는지 확인합니다.
    *   유효하면 `int(a) * int(b)`를 반환하고, 그렇지 않으면 `0`을 반환합니다.

2.  **`solution(input_data)` 함수**:
    *   입력 데이터를 단일 문자열로 합칩니다.
    *   `front_pointer`를 사용하여 문자열 내에서 "mul(" 부분 문자열을 반복적으로 검색합니다 (`input_data.find("mul(", front_pointer)`).
    *   "mul("을 찾으면, 해당 위치에서부터 닫는 괄호 ")"의 위치를 찾습니다 (`input_data.find(")", front_pointer)`).
    *   "mul("부터 해당 ")"까지의 부분 문자열 (예: "mul(10,20)")을 `mul()` 함수에 전달하여 곱셈 결과를 얻습니다.
    *   이 결과를 총합 `result`에 더합니다.
    *   다음 검색을 위해 `front_pointer`를 1 증가시켜 계속 진행합니다.
    *   더 이상 "mul("을 찾을 수 없으면 루프를 종료하고 `result`를 반환합니다.

### Part 1 - 정규 표현식 방식 (`part_1_with_regex.py`)

1.  **`solution(input_data)` 함수**:
    *   입력 데이터를 단일 문자열로 합칩니다.
    *   정규 표현식 `r"mul\((\d+),(\d+)\)"`을 사용하여 "mul(숫자1,숫자2)" 패턴과 일치하는 모든 부분을 찾습니다.
        *   `\d+`는 하나 이상의 숫자를 의미하며, 괄호 `()`는 캡처 그룹을 만들어 숫자 부분만 추출합니다.
        *   `re.findall()` 함수는 일치하는 모든 부분에서 캡처된 그룹들(여기서는 `(숫자1_문자열, 숫자2_문자열)`)의 리스트를 반환합니다.
    *   반환된 리스트의 각 `(a, b)` 튜플에 대해, `a`와 `b`를 정수로 변환하고 곱한 후, 이들의 총합을 계산하여 반환합니다.

## Part 2

Part 2의 목표는 Part 1과 유사하게 "mul(숫자1,숫자2)" 연산의 합을 구하는 것이지만, 추가 조건이 있습니다: "mul" 연산은 가장 최근에 나타난 "do()" 또는 "don't()" 명령의 상태에 따라 수행됩니다. "mul" 앞에 "don't()"보다 "do()"가 더 최근에 나타났거나, "do()"만 있고 "don't()"가 없거나, 둘 다 없는 경우에만 "mul" 연산이 활성화됩니다.

### Part 2 - 수동 파싱 방식 (`part_2_with_parse.py`)

1.  **`mul(string)` 함수**: Part 1의 파싱 방식과 동일합니다.

2.  **`solution(input_data)` 함수**:
    *   "mul(...)" 부분 문자열을 찾는 로직은 Part 1의 파싱 방식과 유사합니다.
    *   각 "mul(...)" 부분 문자열 (`input_data[front_pointer : back_pointer + 1]`)을 찾을 때마다 다음을 수행합니다:
        *   현재 "mul("이 시작되는 위치(`front_pointer`) 이전에 마지막으로 나타난 "do()"의 인덱스(`last_do`)를 찾습니다 (`input_data.rfind("do()", 0, front_pointer)`).
        *   마찬가지로 마지막 "don't()"의 인덱스(`last_do_not`)를 찾습니다.
        *   만약 `last_do >= last_do_not` 조건을 만족하면 (즉, "do" 상태이면), 해당 "mul(...)" 부분 문자열에 대해 `mul()` 함수를 호출하여 결과를 `result`에 더합니다.
            *   `rfind`는 부분 문자열을 찾지 못하면 -1을 반환합니다. 이 로직은 "do()"만 있거나("don't()"는 -1), 둘 다 없거나(-1 >= -1), "do()"가 "don't()"보다 뒤에 나오는 경우를 올바르게 처리합니다.
    *   모든 검색이 끝나면 `result`를 반환합니다.

### Part 2 - 정규 표현식 방식 (`part_2_with_regex.py`)

1.  **`solution(input_data)` 함수**:
    *   입력 데이터를 단일 문자열로 합칩니다.
    *   정규 표현식 `r"mul\((\d+),(\d+)\)"`과 함께 `re.finditer()`를 사용하여 "mul(숫자1,숫자2)" 패턴과 일치하는 모든 부분을 찾습니다. `re.finditer()`는 각 일치 항목에 대한 매치 객체(match object)의 반복자(iterator)를 반환하며, 각 매치 객체는 일치한 문자열의 시작 위치(`mul_match.start()`)와 캡처된 그룹(`mul_match.group(1)`은 숫자1, `mul_match.group(2)`은 숫자2) 정보를 포함합니다.
    *   각 `mul_match`에 대해:
        *   매치된 "mul("의 시작 위치 (`mul_match.start()`)를 기준으로 이전의 마지막 "do()"와 "don't()"의 위치를 `rfind`를 사용하여 찾습니다 (Part 2의 파싱 방식과 동일한 로직).
        *   만약 `last_do >= last_do_not` 조건을 만족하면 ("do" 상태), `mul_match.group(1)`과 `mul_match.group(2)`로부터 두 숫자를 정수로 변환하여 곱하고, 그 결과를 `result`에 더합니다.
    *   모든 일치 항목 처리가 끝나면 `result`를 반환합니다.The `README.md` file for `2024/day_3/` did not exist.
I have read and understood the logic for all four solution files:
-   `part_1_with_parse.py`: Finds "mul(a,b)" substrings by manual string searching (`find`) and sums `a*b`.
-   `part_1_with_regex.py`: Finds "mul(a,b)" substrings using `re.findall(r"mul\((\d+),(\d+)\)")` and sums `a*b`.
-   `part_2_with_parse.py`: Similar to `part_1_with_parse.py`, but before summing `a*b`, it checks if the last "do()" occurrence before the "mul" is more recent than the last "don't()" occurrence. If so (or if "do()" exists and "don't()" doesn't, or neither exists), the product is added.
-   `part_2_with_regex.py`: Similar to `part_1_with_regex.py` (using `re.finditer` to get match objects including start indices), but includes the same "do()"/"don't()" state check as `part_2_with_parse.py` before summing the product.

I have now created the `2024/day_3/README.md` file with detailed explanations in Korean for all four solutions, differentiating between the parsing and regex methods for both Part 1 and Part 2, and using appropriate markdown formatting.
