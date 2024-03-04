import sys

from PySide6 import QtCore, QtWidgets, QtWebEngineWidgets, QtGui
import plotly.express as px
import plotly.graph_objects as go
from utils import *
from ui_mainwindow import Ui_MainWindow
from manager import Manager


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QtGui.QFont(["Open Sans", "verdana", "arial", "sans-serif"]))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.manager: Manager | None = None
        self.ui.actionOpen.triggered.connect(self.show_graph)


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
        colors = px.colors.qualitative.Pastel1
        custom_data = [[f'<br><b>Деталь:</b> {df.loc[i, "task"]}' for i in df.index],
                       [f'<br><b>Начало:</b> {df.loc[i, "start"]}' for i in df.index],
                       [f'<br><b>Длительность:</b> {df.loc[i, "duration"]}' for i in df.index],
                       [f'<br><b>Конец:</b> {df.loc[i, "end"]}' for i in df.index]]
        fig = px.bar(
            df, base="start", x="duration", y="resource", color=df.loc[:, "task"].astype(str), orientation="h", hover_name="task",
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
        tab = QtWidgets.QWidget(self.ui.tabWidget)
        vlayuot = QtWidgets.QVBoxLayout(tab)
        tab.setLayout(vlayuot)
        browser = QtWebEngineWidgets.QWebEngineView()
        browser.setHtml(fig.to_html(include_plotlyjs="cdn"))
        # browser.setHtml("hello")
        vlayuot.addWidget(browser)
        sequence = "-".join(map(lambda x: str(x + 1), [*range(rows)]))
        downtime = Manager.get_downtime(Manager.get_start_end(tasks_matrix, rows, cols))
        label = QtWidgets.QLabel(f"Последовательность: {sequence}", tab)
        label1 = QtWidgets.QLabel(f"Время обработки: {matr[-1][-1]}\t Время простоя: {downtime}", tab)
        sizePolicy1 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        label.setSizePolicy(sizePolicy1)
        label1.setSizePolicy(sizePolicy1)
        font = QtGui.QFont(["Open Sans", "verdana", "arial", "sans-serif"], 11, 8)
        label1.setFont(font)
        label.setFont(font)
        vlayuot.addWidget(label, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        vlayuot.addWidget(label1, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.ui.tabWidget.addTab(tab, 'tab1')


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    main_window.showMaximized()
    sys.exit(app.exec())
