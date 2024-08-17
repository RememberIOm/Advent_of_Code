def cal_case_num(spring):
    broken_springs, conditions = spring
    broken_springs_len, conditions_len = len(broken_springs), len(conditions)

    conditions_prefix_sum = [0] * (conditions_len + 1)
    for i in range(1, conditions_len + 1):
        conditions_prefix_sum[i] = conditions_prefix_sum[i - 1] + conditions[i - 1]

    dp_table = [[0] * (broken_springs_len + 1) for _ in range(conditions_len + 1)]
    dp_table[0][0] = 1

    for i in range(conditions_len + 1):
        cur_condition = conditions[i - 1] if i > 0 else 0
        cur_condition_prefix_sum = conditions_prefix_sum[i]

        for j in range(1, broken_springs_len + 1):
            cur_broken_spring = broken_springs[j - 1]

            # 누적합에 의한 조건 확인
            if j < cur_condition_prefix_sum + i - 1:
                continue

            if cur_broken_spring != "#":
                dp_table[i][j] += dp_table[i][j - 1]

            if cur_broken_spring != ".":
                # condition이 0인 경우
                if cur_condition == 0:
                    continue

                # (j - cur_condition + 1, j - 1)만큼의 문자 중 .이 있는 경우 (현재 condition을 만족할 수 없는 경우)
                if any(
                    broken_springs[k - 1] == "."
                    for k in range(j - cur_condition + 1, j)
                ):
                    continue

                # j - cur_condition 문자가 #일 경우 (경계가 될 수 없는 경우)
                if (
                    0 <= j - 1 - cur_condition
                    and broken_springs[j - 1 - cur_condition] == "#"
                ):
                    continue

                if j - cur_condition - 1 >= 0:
                    dp_table[i][j] += dp_table[i - 1][j - cur_condition - 1]
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
