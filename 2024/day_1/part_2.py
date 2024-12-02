def appear_count(nums):
    counts = {}

    for num in nums:
        counts[num] = counts.get(num, 0) + 1

    return counts


def solution(input_data):
    # Parse input data
    lines = (map(int, line.split()) for line in input_data)
    left_nums, right_nums = map(list, zip(*lines))

    # Sort numbers in each pair
    left_nums, right_nums = map(sorted, (left_nums, right_nums))

    # Appear count of each number in the right list
    right_counts = appear_count(right_nums)

    # Calculate the product of left and the appear count of left in the right list
    mul_appear_counts = (
        left * right_counts.get(left, 0) for left, right in zip(left_nums, right_nums)
    )

    return sum(mul_appear_counts)


INPUT_FILE_PATH = "input.txt"

with open(INPUT_FILE_PATH, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
