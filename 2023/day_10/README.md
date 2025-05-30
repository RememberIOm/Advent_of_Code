# 2023년 Day 10 Advent of Code 문제 풀이

## Part 1

### 문제 설명

Part 1 문제의 목표는 주어진 파이프 미로에서 시작 지점 'S'를 포함하는 메인 루프를 찾고, 이 루프 상에서 시작 지점으로부터 가장 멀리 떨어진 지점까지의 거리를 계산하는 것입니다. 거리는 파이프 구간을 따라 이동하는 단계 수로 측정됩니다.

### 풀이 방법

`part_1.py` 코드는 다음 단계를 통해 문제를 해결합니다.

1.  **그래프 표현**: 입력된 미로를 그래프로 변환합니다. 각 파이프 문자(예: '|', '-', 'L', 'J', '7', 'F')는 해당 파이프가 연결될 수 있는 방향을 나타내는 비트마스크 값으로 매핑됩니다. 'S'는 시작 지점을 나타내며, 초기에는 모든 방향으로 연결 가능한 것으로 간주됩니다. `direction` 열거형 (UP, DOWN, LEFT, RIGHT)을 사용하여 방향을 명확하게 관리합니다.

2.  **시작 지점 탐색**: `get_start_point(graph)` 함수는 그래프를 순회하여 시작 지점 'S'의 좌표 (y, x)를 찾습니다.

3.  **최대 거리 계산 (BFS)**: `get_farthest_step(graph)` 함수는 너비 우선 탐색(BFS) 알고리즘을 사용하여 시작 지점 'S'로부터 가장 멀리 떨어진 지점까지의 거리를 찾습니다.
    *   BFS 큐에는 `(y, x, step_count)` 튜플이 저장되며, `step_count`는 현재 위치까지의 거리를 나타냅니다.
    *   `visited` 2차원 배열은 이미 방문한 파이프를 추적하여 무한 루프 및 중복 계산을 방지합니다.
    *   탐색 과정에서 각 파이프에 대해 다음을 확인합니다:
        *   현재 파이프에서 특정 방향으로 나갈 수 있는지 (비트마스크 확인).
        *   다음 위치가 그래프 범위 내에 있는지.
        *   다음 위치의 파이프가 현재 파이프 쪽으로 연결될 수 있는지 (양방향 연결 확인).
        *   다음 위치가 아직 방문하지 않은 곳인지.
    *   모든 조건이 충족되면 다음 위치를 큐에 추가하고 `visited`에 표시하며, `step_count`를 1 증가시킵니다.
    *   BFS를 진행하면서 만나는 `step_count` 중 최댓값이 기록되며, 이 값이 최종 결과가 됩니다.

4.  **메인 로직**: `solution(input_data)` 함수는 입력 데이터를 받아 그래프를 초기화하고, `get_farthest_step` 함수를 호출하여 결과를 반환합니다. 스크립트는 "input.txt" 파일에서 입력을 읽어 이 함수를 실행하고 결과를 출력합니다.

## Part 2

### 문제 설명

Part 2 문제의 목표는 Part 1에서 식별된 메인 루프에 의해 완전히 둘러싸인 타일의 개수를 세는 것입니다.

### 풀이 방법

`part_2.py` 코드는 Part 1과 유사한 그래프 표현 및 시작 지점 탐색 방식을 사용하지만, 둘러싸인 타일 수를 계산하는 접근 방식이 다릅니다.

1.  **루프 경로 식별 및 내부 후보 표시**: `get_inner_num(graph)` 함수가 핵심 로직을 수행합니다.
    *   시작 지점 'S'에서 출발하여 메인 루프를 따라 이동합니다. Part 1의 BFS와 유사하지만, 루프를 한 방향으로 일관되게 따라가기 위해 약간 수정된 탐색(첫 번째 유효한 다음 단계만 따라감)을 사용합니다.
    *   `loops` 2차원 배열은 메인 루프에 속하는 파이프의 위치를 `True`로 표시합니다.
    *   `near_inners` 2차원 배열은 루프를 특정 방향으로 순회할 때 파이프 경로의 "오른쪽" (또는 특정 상대적 방향)에 있는 타일을 `True`로 표시하려고 시도합니다. 이는 루프의 경계 중 한쪽을 식별하는 데 사용됩니다.

2.  **이미지 생성**:
    *   `loops` 배열과 `near_inners` 배열의 정보를 바탕으로 `fill_before.png`라는 이미지를 생성합니다.
    *   `Pillow` (PIL) 라이브러리와 `numpy`를 사용하여 이미지를 만듭니다.
    *   루프 자체 (`loops`가 `True`인 타일)는 흰색으로 표시됩니다.
    *   루프에 인접한 내부 후보 타일 (`near_inners`가 `True`인 타일)은 빨간색으로 표시됩니다.

3.  **수동 처리**: 코드 주석 `# 이후 포토샵으로 답을 구함` ("After this, the answer is found using Photoshop")에서 알 수 있듯이, 프로그램은 둘러싸인 타일의 수를 직접 계산하지 않습니다. 대신, 생성된 `fill_before.png` 이미지를 이미지 편집 프로그램(예: 포토샵)에서 열어 사용자가 직접 빨간색 영역(내부 후보) 중 실제로 루프에 의해 둘러싸인 부분을 식별하고 채우기 도구(flood fill) 등을 사용하여 개수를 세는 수동 단계를 거칩니다. `fill_after.png` 파일은 이 수동 채우기 작업 후의 상태를 나타내는 이미지일 가능성이 높습니다 (코드 자체에서 생성되지는 않음).

4.  **메인 로직**: `solution(input_data)` 함수는 그래프를 설정하고 `get_inner_num` 함수를 호출하여 이미지 생성 프로세스를 시작합니다. 최종적인 수치적 답은 프로그램 외부에서 얻습니다.

### 이미지 파일

*   `fill_before.png`: `part_2.py` 스크립트에 의해 생성되는 이미지입니다. 메인 파이프 루프는 흰색으로, 루프의 한쪽 면에 인접한 타일들(내부 공간일 가능성이 있는 후보들)은 빨간색으로 표시됩니다. 이 이미지는 내부 타일 개수를 시각적으로 분석하고 수동으로 계산하기 위한 중간 단계 역할을 합니다.
*   `fill_after.png`: (이 저장소에 존재한다면) `fill_before.png` 이미지를 기반으로 이미지 편집 소프트웨어에서 내부 영역을 채운 후의 모습을 보여주는 파일일 것입니다. 이를 통해 둘러싸인 타일의 최종 개수를 확인할 수 있습니다.
