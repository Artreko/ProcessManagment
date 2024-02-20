from copy import copy, deepcopy
from utils import *
import plotly
import plotly.express as px

if __name__ == "__main__":
    filename = "tasks2.txt"

    with open(filename, 'r') as inpfile:
        rows = int(inpfile.readline())
        cols = int(inpfile.readline())
        tasks_matrix = [[*map(int, inpfile.readline().split())] for _ in range(rows)]
    print("Исходная матрица")
    print(*tasks_matrix, sep="\n")
    matr = get_filled_matrix(tasks_matrix)
    print("Исходный результат", matr[-1][-1])

    plot_ranges = get_start_duration(tasks_matrix)
    print(*plot_ranges, sep='\n')
    # посроение диаграммы plotly
    df = get_plot_dataframe(plot_ranges, [*range(rows)])
    custom_data = [[f'<br><b>Деталь:</b> {df.loc[i, "task"]}' for i in df.index],
                   [f'<br><b>Начало:</b> {df.loc[i, "start"]}' for i in df.index],
                   [f'<br><b>Длительность:</b> {df.loc[i, "duration"]}' for i in df.index],
                   [f'<br><b>Конец:</b> {df.loc[i, "end"]}'for i in df.index]]
    fig = px.bar(
        df, base="start", x="duration", y="resource", color=df.task.astype(str), orientation="h", hover_name="task",
        log_x=False, log_y=False, custom_data=custom_data, title="Исходная последовательность",
        labels={
            "resource": "Станок",
            "duration": "Длительность",
            "color": "Деталь"
        }
    ).update_layout(showlegend=True, yaxis_type="category")
    fig.update_yaxes(autorange='reversed')
    fig.update_traces(
        hovertemplate='%{customdata}<extra></extra>')
    fig.select_legends()
    plotly.offline.plot(fig, filename='gantt.html', auto_open=False)

    # получение времени простоя
    start_end = get_start_end(matr)
    print("Начало - Конец")
    print(*start_end, sep="\n")
    downtime = 0
    for resource in start_end:
        for task in resource:
            downtime = downtime + task[0] - task[1]
        downtime += resource[-1][1]
    print("Время простоя", downtime)

    head_sums = [(idx, sum(row[:-1])) for idx, row in enumerate(tasks_matrix)]
    tail_sums = [(idx, sum(row[1:])) for idx, row in enumerate(tasks_matrix)]
    diffs = [(idx, row[-1] - row[0]) for idx, row in enumerate(tasks_matrix)]

    head_sums = sorted(head_sums, key=lambda x: x[1])
    tail_sums = sorted(tail_sums, key=lambda x: x[1], reverse=True)
    diffs = sorted(diffs, key=lambda x: x[1], reverse=True)

    head_sums = [idx for idx, _ in head_sums]
    tail_sums = [idx for idx, _ in tail_sums]
    diffs = [idx for idx, _ in diffs]

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

    head_queue = get_filled_matrix(head_queue)
    tail_queue = get_filled_matrix(tail_queue)
    diffs_queue = get_filled_matrix(diffs_queue)

    print("\nМатрица 1 очереди")
    print(*head_queue, sep="\n")
    print("Время окончания:", head_queue[-1][-1])
    print("\nМатрица 2 очереди")
    print(*tail_queue, sep="\n")
    print("Время окончания:", tail_queue[-1][-1])
    print("\nМатрица 3 очереди")
    print(*diffs_queue, sep="\n")
    print("Время окончания:", diffs_queue[-1][-1])
