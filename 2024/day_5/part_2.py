from collections import deque


def topological_sort(ordering_rules):
    in_degree = {}
    graph = {}

    for parent, child in ordering_rules:
        # Add the parent and child to the graph
        if parent not in graph:
            graph[parent] = []
        graph[parent].append(child)

        # Add the parent and child to the in_degree
        if parent not in in_degree:
            in_degree[parent] = 0

        if child not in in_degree:
            in_degree[child] = 0
        in_degree[child] += 1

    # Find the nodes with in_degree 0
    queue = deque((node for node, degree in in_degree.items() if degree == 0))

    sorted_nodes = []

    # Perform a topological sort
    while queue:
        node = queue.popleft()

        sorted_nodes.append(node)

        for child in graph.get(node, []):
            in_degree[child] -= 1

            if in_degree[child] == 0:
                queue.append(child)

    return sorted_nodes


def solution(input_data):
    ordering_rules = []
    pages = []

    for line in input_data:
        if "|" in line:
            ordering_rules.append(line)
        elif "," in line:
            pages.append(line)

    ordering_rules = tuple(rule.split("|") for rule in ordering_rules)
    pages = tuple(page.split(",") for page in pages)

    invalid_pages_median_sum = 0

    for page in pages:
        # Filter the rules that are valid for the page
        filtered_rules = tuple(
            filter(
                lambda rule: all(rule_element in page for rule_element in rule),
                ordering_rules,
            )
        )

        sorted_page = topological_sort(filtered_rules)

        # If the page is not sorted, add the median to the sum
        if sorted_page != page:
            invalid_pages_median_sum += int(sorted_page[len(sorted_page) // 2])

    return invalid_pages_median_sum


INPUT_FILE_PATH = "input.txt"

with open(INPUT_FILE_PATH, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
