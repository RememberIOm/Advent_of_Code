from math import lcm


def get_cycle_len(ghost, graph, route):
    steps = 0
    cur_node = ghost

    while cur_node[-1] != "Z":
        cur_move = route[steps % len(route)]
        cur_node = graph[cur_node][0 if cur_move == "L" else 1]
        steps += 1

    # input 계산 결과 시작 지점부터 첫 Z 노드까지의 거리와
    # Z 노드부터 다시 Z 노드까지 도달하는 거리가 동일함
    # 따라서 시작 지점부터 첫 Z 노드까지의 거리만 계산하면 됨

    # z_node = cur_node
    # z_node_step = steps

    # while cur_node != z_node or steps == z_node_step:
    #     cur_move = route[steps % len(route)]
    #     cur_node = graph[cur_node][0 if cur_move == "L" else 1]
    #     steps += 1

    # cycle_step = steps - z_node_step

    # return z_node_step, cycle_step

    return steps


def solution(input_data):
    route = input_data[0]

    graph = {}
    ghosts = []

    for line in input_data[2:]:
        graph[line.split(" = ")[0]] = line.split(" = ")[1][1:-1].split(", ")
        if line.split(" = ")[0][-1] == "A":
            ghosts.append(line.split(" = ")[0])

    ghosts_cycle_len = map(lambda ghost: get_cycle_len(ghost, graph, route), ghosts)

    return lcm(*ghosts_cycle_len)


input_file = "input.txt"

with open(input_file, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
