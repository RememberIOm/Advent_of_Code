def mul(string):
    nums = string[4:-1].split(",")

    # Check if the string contains two numbers
    if len(nums) == 2 and all(map(str.isdigit, nums)):
        return int(nums[0]) * int(nums[1])

    return 0


def solution(input_data):
    # Join the input data into a single string
    input_data = "".join(input_data)

    result = 0

    front_pointer = 0
    back_pointer = 0

    while True:
        # Find the next "mul(" substring
        front_pointer = input_data.find("mul(", front_pointer)
        if front_pointer == -1:
            break

        # Find the closing parenthesis
        back_pointer = input_data.find(")", front_pointer)
        if back_pointer == -1:
            break

        result += mul(input_data[front_pointer : back_pointer + 1])

        front_pointer = front_pointer + 1

    return result


INPUT_FILE_PATH = "input.txt"

with open(INPUT_FILE_PATH, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
