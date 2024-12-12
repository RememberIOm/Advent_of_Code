from multiprocessing import pool
from tqdm import tqdm

DIRECTIONS = "^>v<"
DIRECTIONS_MAP = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def check_loop(args):
    grid, cur_x, cur_y, start_x, start_y, start_direction = args

    grid[cur_y][cur_x] = "#"

    result = is_loop(grid, start_x, start_y, start_direction)

    grid[cur_y][cur_x] = "."

    return result


def is_loop(grid, start_x, start_y, start_direction):
    x, y, direction = start_x, start_y, start_direction

    visited_positions = set()

    rows, cols = len(grid), len(grid[0])

    while 0 <= x < cols and 0 <= y < rows:
        if grid[y][x] != "#":
            dx, dy = DIRECTIONS_MAP[direction]
            x += dx
            y += dy
        else:
            dx, dy = DIRECTIONS_MAP[direction]
            x -= dx
            y -= dy

            current_state = (x, y, direction)

            if current_state in visited_positions:
                return True

            visited_positions.add(current_state)

            direction = (direction + 1) % 4

            dx, dy = DIRECTIONS_MAP[direction]
            x += dx
            y += dy

    return False


def solution(input_data):
    data_grid = [list(row) for row in input_data]

    start_x, start_y, start_direction = None, None, None

    for cur_y, row in enumerate(data_grid):
        for cur_x, cell in enumerate(row):
            if cell in DIRECTIONS:
                start_x, start_y, start_direction = cur_x, cur_y, DIRECTIONS.index(cell)
                break
        if start_x is not None:
            break

    dot_cells = [
        (x, y)
        for y, row in enumerate(data_grid)
        for x, cell in enumerate(row)
        if cell == "."
    ]

    tasks = [(data_grid, x, y, start_x, start_y, start_direction) for x, y in dot_cells]

    with pool.Pool() as p:
        results = list(tqdm(p.imap(check_loop, tasks), total=len(tasks)))

    return sum(results)


if __name__ == "__main__":
    INPUT_FILE_PATH = "input.txt"

    with open(INPUT_FILE_PATH, "r") as file:
        data = [line.rstrip() for line in file]

    print(solution(data))
