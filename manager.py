from copy import copy, deepcopy
import pandas as pd
import numpy as np
import plotly
import plotly.express as px


class Manager:
    DATAFRAME_COLUMNS = ["resource", "task", "start", "duration", "end"]

    def __init__(self, mtrx, rows, cols):
        self.tasks_count = rows
        self.resources_count = cols
        self.mtrx = mtrx
        self.tr_matrix = self.transpose(mtrx)

        self.__min_first = None
        self.__max_last = None
        self.__bottle_neck = None
        self.__max_sum = None
        self.__result = None
        self.__head_sums = None
        self.__tail_sums = None
        self.__diffs = None

    @staticmethod
    def read_from_txt(filename):
        with open(filename, 'r') as inpfile:
            rows = int(inpfile.readline())
            cols = int(inpfile.readline())
            tasks_matrix = [[*map(int, inpfile.readline().split())] for _ in range(rows)]
            return Manager(tasks_matrix, rows, cols)

    def get_sequences(self) -> dict[str, list[int]]:
        return {
            "Исходная последовательность": [*range(self.tasks_count)],
            "Первое обобщение Джонсона": self.min_first_sequence,
            "Второе обобщение Джонсона": self.max_last_sequence,
            "Третье обобщение Джонсона": self.bottle_neck_sequence,
            "Четвертое обобщение Джонсона": self.max_sum_sequence,
            "Пятое обобщение Джонсона": self.result_sequence,
            "По сумме первых": self.head_sums_sequence,
            "По сумме последних": self.tail_sums_sequence,
            "По разности": self.diffs_sequence
        }

    # Джонсон
    @property
    def min_first_sequence(self):
        if self.__min_first is not None:
            return self.__min_first
        self.__min_first = sorted(enumerate(self.tr_matrix[0]), key=lambda x: x[1])
        self.__min_first = self.get_sequence(self.__min_first)
        return self.__min_first

    @property
    def max_last_sequence(self):
        if self.__max_last is not None:
            return self.__max_last
        self.__max_last = sorted(enumerate(self.tr_matrix[-1]), key=lambda x: x[1], reverse=True)
        self.__max_last = self.get_sequence(self.__max_last)
        return self.__max_last

    @property
    def bottle_neck_sequence(self):
        if self.__bottle_neck is not None:
            return self.__bottle_neck
        self.__bottle_neck = []
        for row in range(len(self.mtrx)):
            max_col = 0
            max_value = self.mtrx[row][0]
            for col in range(1, self.resources_count):
                value = self.mtrx[row][col]
                if value > max_value:
                    max_value = value
                    max_col = col
            self.__bottle_neck.append((row, max_col))
        self.__bottle_neck.sort(key=lambda x: self.tr_matrix[0][x[0]])
        self.__bottle_neck.sort(key=lambda x: x[1], reverse=True)
        self.__bottle_neck = self.get_sequence(self.__bottle_neck)
        return self.__bottle_neck

    @property
    def max_sum_sequence(self):
        if self.__max_sum is not None:
            return self.__max_sum
        self.__max_sum = sorted(enumerate([sum(row) for row in self.mtrx]), key=lambda x: x[1], reverse=True)
        self.__max_sum = self.get_sequence(self.__max_sum)
        return self.__max_sum

    @property
    def result_sequence(self):
        if self.__result is not None:
            return self.__result
        self.__result = []
        orders = [
            self.min_first_sequence,
            self.max_last_sequence,
            self.bottle_neck_sequence,
            self.max_sum_sequence
        ]
        for i in range(self.tasks_count):
            self.__result.append([i, 0])
            for j in range(self.tasks_count):
                for order in orders:
                    if i == order[j]:
                        self.__result[i][1] += j
        self.__result.sort(key=lambda x: x[1])
        self.__result = self.get_sequence(self.__result)
        return self.__result
    # Джонсон

    # Петров-Соколицын
    @property
    def head_sums_sequence(self):
        if self.__head_sums is not None:
            return self.__head_sums
        self.__head_sums = [(idx, sum(row[:-1])) for idx, row in enumerate(self.mtrx)]
        self.__head_sums = sorted(self.__head_sums, key=lambda x: x[1])
        self.__head_sums = self.get_sequence(self.__head_sums)
        return self.__head_sums

    @property
    def tail_sums_sequence(self):
        if self.__tail_sums is not None:
            return self.__tail_sums
        self.__tail_sums = [(idx, sum(row[1:])) for idx, row in enumerate(self.mtrx)]
        self.__tail_sums = sorted(self.__tail_sums, key=lambda x: x[1], reverse=True)
        self.__tail_sums = self.get_sequence(self.__tail_sums)
        return self.__tail_sums

    @property
    def diffs_sequence(self):
        if self.__diffs is not None:
            return self.__diffs
        self.__diffs = [(idx, row[-1] - row[0]) for idx, row in enumerate(self.mtrx)]
        self.__diffs = sorted(self.__diffs, key=lambda x: x[1], reverse=True)
        self.__diffs = self.get_sequence(self.__diffs)
        return self.__diffs

    # Петров-Соколицын

    def get_sorted_matrix(self, sequence):
        return [copy(self.mtrx[idx]) for idx in sequence]

    @staticmethod
    def get_plot_dataframe(start_duration, tasks_count, resources_count, sequence):
        plot_data = [[] for _ in range(5)]
        for i in range(resources_count):
            for j in range(tasks_count):
                plot_data[0].append(i + 1)
                plot_data[1].append(sequence[j] + 1)
                plot_data[2].append(start_duration[i][j][0])
                plot_data[3].append(start_duration[i][j][1])
                plot_data[4].append(start_duration[i][j][0] + start_duration[i][j][1])

        df = pd.DataFrame(
            np.c_[
                *plot_data
            ],
            columns=Manager.DATAFRAME_COLUMNS
        )
        return df

    @staticmethod
    def plot(df, title):
        custom_data = [[f'<br><b>Деталь:</b> {df.loc[i, Manager.DATAFRAME_COLUMNS[1]]}' for i in df.index],
                       [f'<br><b>Начало:</b> {df.loc[i, Manager.DATAFRAME_COLUMNS[2]]}' for i in df.index],
                       [f'<br><b>Длительность:</b> {df.loc[i, Manager.DATAFRAME_COLUMNS[3]]}' for i in df.index],
                       [f'<br><b>Конец:</b> {df.loc[i, Manager.DATAFRAME_COLUMNS[4]]}' for i in df.index]]
        fig = px.bar(
            df, base=Manager.DATAFRAME_COLUMNS[2], x=Manager.DATAFRAME_COLUMNS[3],
            y=Manager.DATAFRAME_COLUMNS[0], color=df.loc[:, Manager.DATAFRAME_COLUMNS[1]].astype(str), orientation="h",
            custom_data=custom_data, title=title,
            labels={
                Manager.DATAFRAME_COLUMNS[0]: "Станок",
                Manager.DATAFRAME_COLUMNS[3]: "Длительность",
                "color": "Деталь"
            }
        ).update_layout(showlegend=True, yaxis_type="category")
        fig.update_yaxes(autorange='reversed')
        fig.update_xaxes(range=[0, df.loc[df.index[-1], Manager.DATAFRAME_COLUMNS[4]]])
        fig.update_traces(
            hovertemplate='%{customdata}<extra></extra>')
        fig.update_layout(legend_orientation="h")
        fig.select_legends()
        # plotly.offline.plot(fig, filename=f'{"_".join(title.split())}_gantt.html', auto_open=False)
        return fig

    @staticmethod
    def get_filled_matrix(mtrx, tasks_count, resources_count):
        res_mtrx = deepcopy(mtrx)
        for row in range(1, tasks_count):
            res_mtrx[row][0] += res_mtrx[row - 1][0]
        for col in range(1, resources_count):
            res_mtrx[0][col] += res_mtrx[0][col - 1]
        for row in range(1, tasks_count):
            for col in range(1, resources_count):
                res_mtrx[row][col] += max(res_mtrx[row - 1][col], res_mtrx[row][col - 1])
        return res_mtrx

    @staticmethod
    def get_start_duration(mtrx, tasks_count, resources_count):
        res_mtrx = deepcopy(mtrx)
        start_duration = [[] for _ in range(resources_count)]
        start_duration[0].append((0, mtrx[0][0]))
        for row in range(1, tasks_count):
            start_duration[0].append((res_mtrx[row - 1][0], res_mtrx[row][0]))
            res_mtrx[row][0] += res_mtrx[row - 1][0]
        for col in range(1, resources_count):
            start_duration[col].append((res_mtrx[0][col - 1], res_mtrx[0][col]))
            res_mtrx[0][col] += res_mtrx[0][col - 1]
        for row in range(1, tasks_count):
            for col in range(1, resources_count):
                start_duration[col].append(
                    (
                        max(res_mtrx[row - 1][col], res_mtrx[row][col - 1]),
                        res_mtrx[row][col]
                    )
                )
                res_mtrx[row][col] += max(res_mtrx[row - 1][col], res_mtrx[row][col - 1])
        return start_duration

    @staticmethod
    def get_start_end(mtrx, tasks_count, resources_count) -> list[list[tuple[int, int]]]:
        res_mtrx = deepcopy(mtrx)
        start_end = [[] for _ in range(resources_count)]
        start_end[0].append((0, mtrx[0][0]))
        for row in range(1, tasks_count):
            res_mtrx[row][0] += res_mtrx[row - 1][0]
            start_end[0].append((res_mtrx[row - 1][0], res_mtrx[row][0]))
        for col in range(1, resources_count):
            res_mtrx[0][col] += res_mtrx[0][col - 1]
            start_end[col].append((res_mtrx[0][col - 1], res_mtrx[0][col]))
        for row in range(1, tasks_count):
            for col in range(1, resources_count):
                res_mtrx[row][col] += max(res_mtrx[row - 1][col], res_mtrx[row][col - 1])
                start_end[col].append(
                    (
                        max(res_mtrx[row - 1][col], res_mtrx[row][col - 1]),
                        res_mtrx[row][col]
                    )
                )
        return start_end

    @staticmethod
    def get_downtime(start_duration):
        downtime = 0
        for resource in start_duration:
            for task in resource:
                downtime = downtime - task[1]
            downtime += sum(resource[-1])
        return downtime

    @staticmethod
    def transpose(mtrx):
        return [[mtrx[row][col] for row in range(len(mtrx))] for col in range(len(mtrx[0]))]

    @staticmethod
    def get_sequence(sequence):
        return [idx for idx, _ in sequence]
