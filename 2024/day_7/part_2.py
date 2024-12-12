from itertools import product


def check_equtaion(equation):
    left, right = equation

    operators_product = product("+*|", repeat=len(right) - 1)

    for operators in operators_product:
        result = right[0]

        for num, operator in zip(right[1:], operators):
            if operator == "+":
                result += num
            elif operator == "*":
                result *= num
            elif operator == "|":
                result = int(str(result) + str(num))

        if result == left:
            return True

    return False


def solution(input_data):
    equations = []
    for line in input_data:
        left, right = line.split(":")
        left = int(left)
        right = list(map(int, right.split()))
        equations.append((left, right))

    checked_equations = filter(check_equtaion, equations)

    return sum(eq[0] for eq in checked_equations)


if __name__ == "__main__":
    INPUT_FILE_PATH = "input.txt"

    with open(INPUT_FILE_PATH, "r") as file:
        data = [line.rstrip() for line in file]

    print(solution(data))
