def solution(input_data):
    # Parse input data
    lines = (map(int, line.split()) for line in input_data)
    left_nums, right_nums = map(list, zip(*lines))

    # Sort numbers in each pair
    left_nums, right_nums = map(sorted, (left_nums, right_nums))

    # Calculate the difference between the two numbers in each pair
    diff_nums = (abs(left - right) for left, right in zip(left_nums, right_nums))

    return sum(diff_nums)


INPUT_FILE_PATH = "input.txt"

with open(INPUT_FILE_PATH, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
