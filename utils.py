from copy import copy, deepcopy
import pandas as pd
import numpy as np


def get_plot_dataframe(plot_ranges, sequence):
    details_count = len(plot_ranges[0])
    machines_count = len(plot_ranges)
    plot_data = [[] for _ in range(5)]
    for i in range(machines_count):
        for j in range(details_count):
            plot_data[0].append(i + 1)
            plot_data[1].append(sequence[j] + 1)
            plot_data[2].append(plot_ranges[i][j][0])
            plot_data[3].append(plot_ranges[i][j][1])
            plot_data[4].append(plot_ranges[i][j][0] + plot_ranges[i][j][1])

    df = pd.DataFrame(
        np.c_[
            *plot_data
        ],
        columns=["resource", "task", "start", "duration", "end"]
    )

    return df


def get_filled_matrix(mtrx):
    res_mtrx = deepcopy(mtrx)
    rows_count = len(res_mtrx)
    cols_count = len(res_mtrx[0])
    for row in range(1, rows_count):
        res_mtrx[row][0] += res_mtrx[row - 1][0]
    for col in range(1, cols_count):
        res_mtrx[0][col] += res_mtrx[0][col - 1]
    for row in range(1, rows_count):
        for col in range(1, cols_count):
            res_mtrx[row][col] += max(res_mtrx[row - 1][col], res_mtrx[row][col - 1])
    return res_mtrx


def get_start_duration(mtrx):
    res_mtrx = deepcopy(mtrx)
    rows_count = len(res_mtrx)
    cols_count = len(res_mtrx[0])
    plot_ranges = [[] for _ in range(cols_count)]
    plot_ranges[0].append((0, mtrx[0][0]))
    for row in range(1, rows_count):
        plot_ranges[0].append((res_mtrx[row - 1][0], res_mtrx[row][0]))
        res_mtrx[row][0] += res_mtrx[row - 1][0]
    for col in range(1, cols_count):
        plot_ranges[col].append((res_mtrx[0][col - 1], res_mtrx[0][col]))
        res_mtrx[0][col] += res_mtrx[0][col - 1]
    for row in range(1, rows_count):
        for col in range(1, cols_count):
            plot_ranges[col].append((max(res_mtrx[row - 1][col], res_mtrx[row][col - 1]),
                                     res_mtrx[row][col]))
            res_mtrx[row][col] += max(res_mtrx[row - 1][col], res_mtrx[row][col - 1])
    return plot_ranges


def get_start_end(mtrx):
    rows_count = len(mtrx)
    cols_count = len(mtrx[0])
    plot_ranges = [[] for _ in range(cols_count)]
    plot_ranges[0].append((0, mtrx[0][0]))
    for row in range(1, rows_count):
        plot_ranges[0].append((mtrx[row - 1][0], mtrx[row][0]))
    for col in range(1, cols_count):
        plot_ranges[col].append((mtrx[0][col - 1], mtrx[0][col]))
    for row in range(1, rows_count):
        for col in range(1, cols_count):
            plot_ranges[col].append((max(mtrx[row - 1][col], mtrx[row][col - 1]), mtrx[row][col]))
    return plot_ranges


def transpose(mtrx):
    return [[mtrx[row][col] for row in range(len(mtrx))] for col in range(len(mtrx[0]))]


def get_sorted_matrix(source, sequence):
    return [copy(source[idx]) for idx in sequence]
