def is_safe(nums):
    # Increasing order -> +
    # Decreasing order -> -
    order = nums[-1] - nums[0]

    for i in range(len(nums) - 1):
        diff = nums[i + 1] - nums[i]

        # Check order
        if (diff) * order <= 0:
            return False

        # Check bounds
        if not (-3 <= diff <= 3) or diff == 0:
            return False

    return True


def solution(input_data):
    # Parse input data
    lines = (tuple(map(int, line.split())) for line in input_data)

    # Check if the difference between the numbers in each pair is safe
    safe_lines = tuple(filter(is_safe, lines))

    return len(safe_lines)


INPUT_FILE_PATH = "input.txt"

with open(INPUT_FILE_PATH, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
