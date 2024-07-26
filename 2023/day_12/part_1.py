from itertools import combinations_with_replacement, permutations


def get_dot_arrangements(broken_spring, arrangement):
    broken_spring_len = len(broken_spring)
    arrangement_len = len(arrangement)
    arrangement_sum = sum(arrangement)

    # 양 끝은 0이 될 수 있기 때문에 가운데 부분을 먼저 구하고 양 끝을 구함
    for center_arrangement in combinations_with_replacement(
        range(1, broken_spring_len - (arrangement_sum) + 1), arrangement_len - 1
    ):
        # 양 끝에 할당되는 공간
        remaining_space = broken_spring_len - (
            arrangement_sum + sum(center_arrangement)
        )

        # 양 끝을 구함
        for h in range(remaining_space + 1):
            for center_arrangement_prod in set(permutations(center_arrangement)):
                dot_arrangement = tuple(
                    [h] + list(center_arrangement_prod) + [remaining_space - h]
                )
                yield dot_arrangement


def get_possible_cases(broken_spring, arrangement):
    dot_arrangements = get_dot_arrangements(broken_spring, arrangement)

    for dot_arrangement in dot_arrangements:
        case_string = ""

        # 나누어지는 공간에 대한 문자열 생성
        for dot_len, sharp_len in zip(dot_arrangement, list(arrangement) + [0]):
            case_string += "." * dot_len + "#" * sharp_len

        yield case_string


def is_broken_spring_cases(broken_spring, case_string):
    for b, c in zip(broken_spring, case_string):
        if b != "?" and b != c:
            return False

    return True


def cal_case_num(spring):
    broken_spring, arrangement = spring

    # 나누어지는 공간에 대한 가능한 문자열 list 생성
    possible_cases = get_possible_cases(broken_spring, arrangement)

    # possible_cases가 broken_spring에 해당하는 경우의 수를 계산
    return sum(
        is_broken_spring_cases(broken_spring, case_string)
        for case_string in possible_cases
    )


def solution(input_data):
    springs = tuple(
        (line.split()[0], tuple(map(int, line.split()[1].split(","))))
        for line in input_data
    )

    return sum(cal_case_num(spring) for spring in springs)


input_file = "input.txt"

with open(input_file, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
