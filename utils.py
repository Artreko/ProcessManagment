from copy import copy


def fill_matrix(mtrx):
    rows_count = len(mtrx)
    cols_count = len(mtrx[0])
    for row in range(1, rows_count):
        mtrx[row][0] += mtrx[row - 1][0]
    for col in range(1, cols_count):
        mtrx[0][col] += mtrx[0][col - 1]
    for row in range(1, rows_count):
        for col in range(1, cols_count):
            mtrx[row][col] += max(mtrx[row - 1][col], mtrx[row][col - 1])


def transponse(mtrx):
    return [[mtrx[row][col] for row in range(len(mtrx))] for col in range(len(mtrx[0]))]


def get_sorted_matrix(source, sequence):
    return [copy(source[el[0]]) for el in sequence]