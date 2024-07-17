def find_num(field, i, j, visited):
    h, t = j, j

    while field[i][h].isdigit():
        h -= 1

    while field[i][t].isdigit():
        t += 1

    for k in range(h + 1, t):
        if visited[i][k]:
            return 0

        visited[i][k] = True

    return int(field[i][h + 1 : t])


def cal_num(input_field):
    input_field_width = len(input_field[0])

    row_padding = "." * (input_field_width + 2)

    field = [row_padding] + [f".{row}." for row in input_field] + [row_padding]

    field_height = len(field)
    field_width = len(field[0])

    answer = 0
    visited = [[False] * field_width for _ in range(field_height)]

    for i in range(1, field_height - 1):
        for j in range(1, field_width - 1):
            if field[i][j].isdigit() or field[i][j] == ".":
                continue

            for dx, dy in (
                (-1, -1),
                (-1, 0),
                (-1, 1),
                (0, -1),
                (0, 1),
                (1, -1),
                (1, 0),
                (1, 1),
            ):
                next_i, next_j = i + dx, j + dy

                if field[next_i][next_j].isdigit():
                    answer += find_num(field, next_i, next_j, visited)

    return answer


input_file = "input.txt"

with open(input_file, "r") as file:
    data = list(map(str.rstrip, file.readlines()))

print(cal_num(data))
