def get_cycle(ghost, graph, route):
    cur_node = ghost

    for route_elem in route:
        cur_node = graph[cur_node][0 if route_elem == "L" else 1]

    cycle = [cur_node]

    while cycle[0] != cur_node or len(cycle) == 1:
        for route_elem in route:
            cur_node = graph[cur_node][0 if route_elem == "L" else 1]
            cycle.append(cur_node)

    return tuple(cycle[:-1])


def get_z_in_cycle(ghost_cycle):
    return (
        list(idx for idx, node in enumerate(ghost_cycle) if node[-1] == "Z"),
        len(ghost_cycle),
    )


def solution(input_data):
    route = input_data[0]

    graph = {}
    ghosts = []

    for line in input_data[2:]:
        graph[line.split(" = ")[0]] = line.split(" = ")[1][1:-1].split(", ")
        if line.split(" = ")[0][-1] == "A":
            ghosts.append(line.split(" = ")[0])

    ghosts_cycle = tuple(map(lambda ghost: get_cycle(ghost, graph, route), ghosts))
    ghosts_z_in_cycle = tuple(
        map(lambda ghost_cycle: get_z_in_cycle(ghost_cycle), ghosts_cycle)
    )

    # TODO: Fix this


input_file = "input.txt"

with open(input_file, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
