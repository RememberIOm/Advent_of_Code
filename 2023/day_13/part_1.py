def get_reflex(pattern):
    max_reflex, max_row = 0, 0

    for start_row in range(1, len(pattern)):
        for delta in range(min(start_row, len(pattern) - start_row)):
            if pattern[start_row - delta - 1] != pattern[start_row + delta]:
                break

            if delta > max_reflex:
                max_reflex = delta
                max_row = start_row - 1

    # 인덱스를 1부터 계산
    max_row += 1

    return max_reflex, max_row


def get_max_reflex(pattern):
    row_reflex, max_row = get_reflex(pattern)
    col_reflex, max_col = get_reflex(tuple(zip(*pattern)))

    if row_reflex > col_reflex:
        return max_row * 100
    else:
        return max_col


def solution(input_data):
    pattern = []
    answer = 0

    for line in input_data + ("",):
        if line == "":
            answer += get_max_reflex(pattern)
            pattern = []
        else:
            pattern.append(line)

    return answer


input_file = "input.txt"

with open(input_file, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
