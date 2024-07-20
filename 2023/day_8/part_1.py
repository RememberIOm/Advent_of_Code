def solution(input_data):
    route = input_data[0]

    graph = {}

    for line in input_data[2:]:
        graph[line.split(" = ")[0]] = line.split(" = ")[1][1:-1].split(", ")

    steps = 0
    cur_node = "AAA"

    while True:
        cur_move = route[steps % len(route)]
        cur_node = graph[cur_node][0 if cur_move == "L" else 1]
        steps += 1

        if cur_node == "ZZZ":
            return steps


input_file = "input.txt"

with open(input_file, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
