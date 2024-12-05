def is_valid_ordering(ordering_rules, page):
    for a, b in ordering_rules:
        if a in page and b in page and page.index(a) > page.index(b):
            return False

    return True


def solution(input_data):
    ordering_rules = []
    pages = []

    for line in input_data:
        if "|" in line:
            ordering_rules.append(line)
        elif "," in line:
            pages.append(line)

    ordering_rules = tuple(tuple(map(int, rule.split("|"))) for rule in ordering_rules)
    pages = tuple(tuple(map(int, page.split(","))) for page in pages)

    valid_pages = filter(lambda page: is_valid_ordering(ordering_rules, page), pages)

    return sum(page[len(page) // 2] for page in valid_pages)


INPUT_FILE_PATH = "input.txt"

with open(INPUT_FILE_PATH, "r") as file:
    data = tuple(map(str.rstrip, file.readlines()))

print(solution(data))
