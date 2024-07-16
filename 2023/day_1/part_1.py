def cal_num(string):
    num_list = [i for i in string if i.isdigit()]

    return int(num_list[0] + num_list[-1])


input_file = "temp.txt"

with open(input_file, "r") as file:
    data = list(map(str.rstrip, file.readlines()))

print(sum(cal_num(i) for i in data))
