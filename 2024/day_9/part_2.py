def data_to_unpacked_block(data):
    filled_blocks = []
    empty_blocks = []

    current_value = 0
    current_index = 0
    is_empty = False

    # data를 block 단위로 나누어 packed data를 unpacked block으로 변환
    for length in data:
        if is_empty:
            empty_blocks.append((".", length, current_index))
        else:
            if length > 0:
                filled_blocks.append((current_value, length, current_index))
            current_value += 1

        current_index += length
        is_empty = not is_empty

    return filled_blocks, empty_blocks


def defragment_blocks(filled_blocks, empty_blocks):
    VALUE, LENGTH, INDEX = 0, 1, 2

    empty_index = 0
    filled_index = len(filled_blocks) - 1

    while empty_index < len(empty_blocks):
        while filled_index >= 0:
            # empty block에 들어갈 수 있는 조건
            # 1. filled block의 길이가 empty block의 길이보다 작거나 같아야 함
            # 2. filled block의 시작 인덱스가 empty block의 시작 인덱스보다 같거나 커야 함
            if (
                empty_blocks[empty_index][LENGTH] >= filled_blocks[filled_index][LENGTH]
            ) and (
                empty_blocks[empty_index][INDEX] <= filled_blocks[filled_index][INDEX]
            ):
                break
            filled_index -= 1

        # filled block이 모두 탐색되었다면 다음 empty block으로 이동
        # (어떤 filled block도 empty block으로 옮길 수 없는 상황)
        if filled_index < 0:
            filled_index = len(filled_blocks) - 1
            empty_index += 1
            continue

        e_value, e_length, e_index = empty_blocks[empty_index]
        f_value, f_length, f_index = filled_blocks[filled_index]

        # current filled block을 empty 공간으로 옮길 수 있는 상황
        # 1. 옮겨진 filled block 정보를 empty block에 추가
        empty_blocks.append((e_value, f_length, f_index))

        # 2. filled block 정보를 empty block 위치로 갱신
        filled_blocks[filled_index] = (f_value, f_length, e_index)

        # 3. empty block 재조정
        empty_blocks[empty_index] = (e_value, e_length - f_length, e_index + f_length)

        # 만약 empty block이 소진되었다면 다음 empty block으로 이동
        if empty_blocks[empty_index][LENGTH] == 0:
            empty_index += 1

        # filled blocks pointer 초기화 후 다시 탐색 시작
        filled_index = len(filled_blocks) - 1

    # 모든 블록을 인덱스 순서대로 정렬
    defraged_blocks = sorted(filled_blocks + empty_blocks, key=lambda x: x[INDEX])

    # 정렬된 블록을 기반으로 최종 데이터 구성
    defraged_data = []
    for value, length, _ in defraged_blocks:
        defraged_data.extend([value] * length)

    return defraged_data


def compute_checksum(data):
    checksum = 0

    for i, cell in enumerate(data):
        if cell != ".":
            checksum += cell * i

    return checksum


def solution(input_data):
    packed_data = list(map(int, input_data[0]))

    filled_blocks, empty_blocks = data_to_unpacked_block(packed_data)

    defraged_data = defragment_blocks(filled_blocks, empty_blocks)

    return compute_checksum(defraged_data)


if __name__ == "__main__":
    INPUT_FILE_PATH = "input.txt"

    with open(INPUT_FILE_PATH, "r") as file:
        data = [line.rstrip() for line in file]

    print(solution(data))
