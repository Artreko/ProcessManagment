from copy import copy, deepcopy
from utils import fill_matrix, transponse, get_sorted_matrix

filename = "tasks2.txt"

with open(filename, 'r') as inpfile:
    rows = int(inpfile.readline())
    cols = int(inpfile.readline())
    tasks_matrix = [[*map(int, inpfile.readline().split())] for _ in range(rows)]

print("Исходная матрица")
print(*tasks_matrix, sep="\n")

print("Транспонированная матрица")
print(*(tr_matrix := transponse(tasks_matrix)), sep="\n")

fill_matrix(filled_matrix := deepcopy(tasks_matrix))

print("Исходный результат", filled_matrix[-1][-1])

min_first_order = sorted(enumerate(tr_matrix[0]), key=lambda x: x[1])
max_last_order = sorted(enumerate(tr_matrix[-1]), key=lambda x: x[1], reverse=True)

bottle_neck_order = []
for row in range(len(tasks_matrix)):
    max_col = 0
    max_value = tasks_matrix[row][0]
    for col in range(1, len(tasks_matrix[0])):
        value = tasks_matrix[row][col]
        if value > max_value:
            max_value = value
            max_col = col
    bottle_neck_order.append((row, max_col))
bottle_neck_order.sort(key=lambda x: tr_matrix[0][x[0]])
bottle_neck_order.sort(key=lambda x: x[1], reverse=True)
max_sum_order = sorted(enumerate([sum(row) for row in tasks_matrix]), key=lambda x: x[1], reverse=True)

sum_order = []
tasks_count = len(tasks_matrix)
orders = [min_first_order, max_last_order, bottle_neck_order, max_sum_order]
for i in range(tasks_count):
    sum_order.append([i, 0])
    for j in range(tasks_count):
        for order in orders:
            if i == order[j][0]:
                sum_order[i][1] += j

print(min_first_order)
fill_matrix(mtr := get_sorted_matrix(tasks_matrix, min_first_order))
print(mtr[-1][-1])
print(max_last_order)
fill_matrix(mtr := get_sorted_matrix(tasks_matrix, max_last_order))
print(mtr[-1][-1])
print(bottle_neck_order)
fill_matrix(mtr := get_sorted_matrix(tasks_matrix, bottle_neck_order))
print(mtr[-1][-1])
print(max_sum_order)
fill_matrix(mtr := get_sorted_matrix(tasks_matrix, max_sum_order))
print(mtr[-1][-1])
sum_order.sort(key=lambda x: x[1])
print(sum_order)
fill_matrix(mtr := get_sorted_matrix(tasks_matrix, sum_order))
print(mtr[-1][-1])
