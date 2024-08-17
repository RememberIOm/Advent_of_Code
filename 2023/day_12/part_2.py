def cal_case_num(spring):
    broken_springs, conditions = spring

    # dp 테이블을 만들기 위해 맨 앞에 0을 추가
    broken_springs = "_" + broken_springs
    conditions = (0,) + conditions

    broken_springs_len, conditions_len = len(broken_springs), len(conditions)

    # conditions의 누적합
    conditions_prefix_sum = [0] * conditions_len
    for i, condition in enumerate(conditions):
        conditions_prefix_sum[i] = conditions_prefix_sum[i - 1] + condition

    dp_table = tuple([0] * broken_springs_len for _ in range(conditions_len))
    dp_table[0][0] = 1

    for i, (condition, condition_prefix_sum) in enumerate(
        zip(conditions, conditions_prefix_sum)
    ):
        for j, broken_spring in enumerate(broken_springs[1:], 1):
            # 누적합에 의한 조건 확인 (#이 들어가는데 필요한 최소 길이)
            if j < condition_prefix_sum + i - 1:
                continue

            if broken_spring != "#":
                dp_table[i][j] += dp_table[i][j - 1]

            if broken_spring != ".":
                # condition이 0인 경우
                if condition == 0:
                    continue

                # [j - condition + 1, j]만큼의 문자 중 .이 있는 경우 (현재 condition을 만족할 수 없는 경우)
                if any(broken_springs[k] == "." for k in range(j - condition + 1, j)):
                    continue

                # j - condition 문자가 #일 경우 (#이 분리될 수 없는 경우)
                if 0 <= j - condition and broken_springs[j - condition] == "#":
                    continue

                if j - condition - 1 >= 0:
                    dp_table[i][j] += dp_table[i - 1][j - condition - 1]
                else:
                    dp_table[i][j] += 1

    return dp_table[-1][-1]


def solution(input_data):
    UNFOLD_SPRING = 5

    springs = tuple(
        (
            ((line.split()[0] + "?") * UNFOLD_SPRING)[:-1],
            tuple(map(int, line.split()[1].split(","))) * UNFOLD_SPRING,
        )
        for line in input_data
    )

    return sum(cal_case_num(spring) for spring in springs)


input_file = "input.txt"

with open(input_file, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
