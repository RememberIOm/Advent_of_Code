from collections import deque


def unpack_data(data):
    unpacked_data = []

    cur_num = 0
    empty_flag = False
    for data_cell in data:
        if empty_flag:
            unpacked_data += ["."] * data_cell
        else:
            if data_cell != 0:
                unpacked_data += [cur_num] * data_cell
            cur_num += 1

        empty_flag = not empty_flag

    return list(unpacked_data)


def defraging(data):
    empty_cell_indices = deque(i for i, cell in enumerate(data) if cell == ".")
    filled_cell_indices = [i for i, cell in enumerate(data) if cell != "."]

    while True:
        cur_empty_cell_index = empty_cell_indices.popleft()
        cur_filled_cell_index = filled_cell_indices.pop()

        if cur_empty_cell_index >= cur_filled_cell_index:
            break

        data[cur_empty_cell_index], data[cur_filled_cell_index] = (
            data[cur_filled_cell_index],
            data[cur_empty_cell_index],
        )

    return data


def get_checksum(data):
    result = 0
    for i, cell in enumerate(data):
        if cell == ".":
            break

        result += cell * i

    return result


def solution(input_data):
    packed_data = list(map(int, input_data[0]))

    unpacked_data = unpack_data(packed_data)

    defraged_data = defraging(unpacked_data)

    return get_checksum(defraged_data)


if __name__ == "__main__":
    INPUT_FILE_PATH = "input.txt"

    with open(INPUT_FILE_PATH, "r") as file:
        data = [line.rstrip() for line in file]

    print(solution(data))
