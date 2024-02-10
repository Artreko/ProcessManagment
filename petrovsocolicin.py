from copy import copy, deepcopy
from utils import fill_matrix, get_sorted_matrix


if __name__ == "__main__":

    filename = "tasks.txt"

    with open(filename, 'r') as inpfile:
        rows = int(inpfile.readline())
        cols = int(inpfile.readline())
        tasks_matrix = [[*map(int, inpfile.readline().split())] for _ in range(rows)]
    print("Исходная матрица")
    print(*tasks_matrix, sep="\n")
    fill_matrix(matr := deepcopy(tasks_matrix))
    print("Исходный результат", matr[-1][-1])

    head_sums = [(idx, sum(row[:-1])) for idx, row in enumerate(tasks_matrix)]
    tail_sums = [(idx, sum(row[1:])) for idx, row in enumerate(tasks_matrix)]
    diffs = [(idx, row[-1] - row[0]) for idx, row in enumerate(tasks_matrix)]

    head_sums = sorted(head_sums, key=lambda x: x[1])
    tail_sums = sorted(tail_sums, key=lambda x: x[1], reverse=True)
    diffs = sorted(diffs, key=lambda x: x[1], reverse=True)

    print("\nПоследовательности")
    print(head_sums)
    print(tail_sums)
    print(diffs)

    head_queue = get_sorted_matrix(tasks_matrix, head_sums)
    tail_queue = get_sorted_matrix(tasks_matrix, tail_sums)
    diffs_queue = get_sorted_matrix(tasks_matrix, diffs)

    print("\nМатрица 1 очереди")
    print(*head_queue, sep="\n")
    print("\nМатрица 2 очереди")
    print(*tail_queue, sep="\n")
    print("\nМатрица 3 очереди")
    print(*diffs_queue, sep="\n")

    fill_matrix(head_queue)
    fill_matrix(tail_queue)
    fill_matrix(diffs_queue)

    print("\nМатрица 1 очереди")
    print(*head_queue, sep="\n")
    print("Время окончания:", head_queue[-1][-1])
    print("\nМатрица 2 очереди")
    print(*tail_queue, sep="\n")
    print("Время окончания:", tail_queue[-1][-1])
    print("\nМатрица 3 очереди")
    print(*diffs_queue, sep="\n")
    print("Время окончания:", diffs_queue[-1][-1])
