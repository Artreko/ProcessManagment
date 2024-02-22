from random import random
from utils import get_filled_matrix, transpose, get_sorted_matrix, get_start_duration
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

if __name__ == "__main__":
    filename = "tasks2.txt"

    with open(filename, 'r') as inpfile:
        rows = int(inpfile.readline())
        cols = int(inpfile.readline())
        tasks_matrix = [[*map(int, inpfile.readline().split())] for _ in range(rows)]

    print("Исходная матрица")
    print(*tasks_matrix, sep="\n")

    print("Транспонированная матрица")
    print(*(tr_matrix := transpose(tasks_matrix)), sep="\n")

    filled_matrix = get_filled_matrix(tasks_matrix)

    print("Матрица построения графика")
    plot_ranges = get_start_duration(tasks_matrix)
    print(*plot_ranges, sep="\n")

    fig, ax = plt.subplots()
    colors = [(random(), random(), random()) for _ in range(rows)]
    labels = [*map(str, range(1, rows+1))]
    patches = [mpatches.Patch(color=colors[i], label=labels[i]) for i in range(rows)]

    # for idx, resource in enumerate(plot_ranges):
    #     ax.broken_barh(resource, (cols-idx-0.4, 0.8), facecolors=

    for r_idx, resource in enumerate(plot_ranges):
        for t_idx, task in enumerate(resource):
            ax.barh(r_idx+1, task[1], 0.8, task[0], label=labels[t_idx], color=colors[t_idx], mouseover=True)

    # ax.invert_yaxis()
    ax.set_xlim(0, filled_matrix[-1][-1]+1)
    ax.set_ylim(0, cols+1)

    plt.legend(handles=patches)
    plt.gca().invert_yaxis()
    plt.show()

    print("Исходный результат", filled_matrix[-1][-1])

    min_first_order = sorted(enumerate(tr_matrix[0]), key=lambda x: x[1])
    min_first_order = [idx for idx, _ in min_first_order]

    max_last_order = sorted(enumerate(tr_matrix[-1]), key=lambda x: x[1], reverse=True)
    max_last_order = [idx for idx, _ in max_last_order]

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
    bottle_neck_order = [idx for idx, _ in bottle_neck_order]

    max_sum_order = sorted(enumerate([sum(row) for row in tasks_matrix]), key=lambda x: x[1], reverse=True)
    max_sum_order = [idx for idx, _ in max_sum_order]

    sum_order = []
    tasks_count = len(tasks_matrix)
    orders = [min_first_order, max_last_order, bottle_neck_order, max_sum_order]
    for i in range(tasks_count):
        sum_order.append([i, 0])
        for j in range(tasks_count):
            for order in orders:
                if i == order[j]:
                    sum_order[i][1] += j
    sum_order.sort(key=lambda x: x[1])
    sum_order = [idx for idx, _ in sum_order]

    print(min_first_order)
    mtr = get_filled_matrix(get_sorted_matrix(tasks_matrix, min_first_order))
    # print(*plot_ranges, sep="\n")
    print(mtr[-1][-1])
    print(max_last_order)
    mtr = get_filled_matrix(get_sorted_matrix(tasks_matrix, max_last_order))
    print(mtr[-1][-1])
    print(bottle_neck_order)
    mtr = get_filled_matrix(get_sorted_matrix(tasks_matrix, bottle_neck_order))
    print(mtr[-1][-1])
    print(max_sum_order)
    mtr = get_filled_matrix(get_sorted_matrix(tasks_matrix, max_sum_order))
    print(mtr[-1][-1])
    print(sum_order)
    mtr = get_filled_matrix(get_sorted_matrix(tasks_matrix, sum_order))
    print(mtr[-1][-1])
