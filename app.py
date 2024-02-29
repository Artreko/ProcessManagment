from PySide6 import QtCore, QtWidgets, QtWebEngineWidgets
import plotly.express as px
from utils import *


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button = QtWidgets.QPushButton('Plot', self)
        self.browser = QtWebEngineWidgets.QWebEngineView(self)

        vlayout = QtWidgets.QVBoxLayout(self)
        vlayout.addWidget(self.button, alignment=QtCore.Qt.AlignHCenter)
        vlayout.addWidget(self.browser)

        self.button.clicked.connect(self.show_graph)
        self.resize(1000,800)

    def show_graph(self):
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
                       [f'<br><b>Конец:</b> {df.loc[i, "end"]}' for i in df.index]]
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
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Widget()
    widget.show()
    app.exec()
