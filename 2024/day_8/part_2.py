def get_antinode(antennas, bounds):
    antinodes = set()

    for antenna, positions in antennas.items():
        for cur_x, cur_y in positions:
            for other_x, other_y in positions:
                if (cur_x, cur_y) == (other_x, other_y):
                    continue

                diff_x = cur_x - other_x
                diff_y = cur_y - other_y

                cur_x_copy, cur_y_copy = cur_x, cur_y
                other_x_copy, other_y_copy = other_x, other_y

                cur_antinodes = []

                while True:
                    other_x_copy += diff_x
                    other_y_copy += diff_y

                    if (other_x_copy, other_y_copy) not in bounds:
                        break

                    cur_antinodes.append((other_x_copy, other_y_copy))
                while True:
                    cur_x_copy -= diff_x
                    cur_y_copy -= diff_y

                    if (cur_x_copy, cur_y_copy) not in bounds:
                        break

                    cur_antinodes.append((cur_x_copy, cur_y_copy))

                antinodes.update(cur_antinodes)

    return antinodes


def solution(input_data):
    antennas = {}
    for y, row in enumerate(input_data):
        for x, cell in enumerate(row):
            if cell != ".":
                antennas.setdefault(cell, []).append((x, y))

    bounds = {(x, y) for y in range(len(input_data)) for x in range(len(input_data[y]))}

    return len(get_antinode(antennas, bounds))


if __name__ == "__main__":
    INPUT_FILE_PATH = "input.txt"

    with open(INPUT_FILE_PATH, "r") as file:
        data = [line.rstrip() for line in file]

    print(solution(data))
