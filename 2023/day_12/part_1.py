from itertools import combinations_with_replacement, permutations, product


def get_dot_arrangements(broken_spring, arrangement):
    broken_spring_len = len(broken_spring)
    arrangement_len = len(arrangement)
    arrangement_sum = sum(arrangement)

    # "#" 사이의 나누어지는 공간
    dot_arrangements = []

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
                dot_arrangements.append(dot_arrangement)

    return dot_arrangements


def get_possible_cases(broken_spring, arrangement):
    dot_arrangements = get_dot_arrangements(broken_spring, arrangement)

    # 나누어지는 공간에 대한 가능한 문자열 set 생성
    possible_cases = set()

    for dot_arrangement in dot_arrangements:
        case_string = ""

        # 나누어지는 공간에 대한 문자열 생성
        for dot_len, sharp_len in zip(dot_arrangement, list(arrangement) + [0]):
            case_string += "." * dot_len + "#" * sharp_len

        possible_cases.add(case_string)

    return possible_cases


def get_broken_spring_cases(broken_spring):
    # broken_spring에 대한 가능한 문자열 set 생성
    broken_spring_cases = set()

    for is_dot_tuple in product((True, False), repeat=broken_spring.count("?")):
        case_string = ""
        is_dot_tuple_iter = iter(is_dot_tuple)

        for c in broken_spring:
            if c == "?":
                case_string += "." if next(is_dot_tuple_iter) else "#"
            else:
                case_string += c

        broken_spring_cases.add(case_string)

    return broken_spring_cases


def cal_case_num(spring):
    broken_spring, arrangement = spring

    # 나누어지는 공간에 대한 가능한 문자열 set 생성
    possible_cases = get_possible_cases(broken_spring, arrangement)

    # broken_spring에 대한 가능한 문자열 set 생성
    broken_spring_cases = get_broken_spring_cases(broken_spring)

    # 가능한 문자열 set의 교집합
    intersection = possible_cases & broken_spring_cases

    return len(intersection)


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
