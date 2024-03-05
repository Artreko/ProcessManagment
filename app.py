import os
import sys

from PySide6 import QtCore, QtWidgets, QtWebEngineWidgets, QtGui
import plotly.express as px

from pagewidget import PageWidget
from ui_mainwindow import Ui_MainWindow
from manager import Manager


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QtGui.QFont(["Open Sans", "verdana", "arial", "sans-serif"]))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.manager: Manager | None = None
        self.ui.actionOpen.triggered.connect(self.open_file_txt)

    def open_file_txt(self):
        self.ui.tabWidget.clear()
        docs_dir = os.path.join(QtCore.QDir.homePath(), "Documents")
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                            "Открыть текстовый файл",
                                                            docs_dir,
                                                            "Text files (*.txt)")
        if filename:
            self.manager = Manager.read_from_txt(filename)
            self.calculate()

    def calculate(self):
        sequences = self.manager.get_sequences()
        for title, sequence in sequences.items():
            mtrx = self.manager.get_sorted_matrix(sequence)
            tasks = self.manager.tasks_count
            res = self.manager.resources_count
            start_duration = Manager.get_start_duration(mtrx, tasks, res)

            df = Manager.get_plot_dataframe(start_duration, tasks, res, sequence)
            fig = Manager.plot(df, title)

            downtime = Manager.get_downtime(start_duration)
            total_time = sum(start_duration[-1][-1])

            self.ui.tabWidget.addTab(PageWidget(fig, sequence, total_time, downtime), title)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    main_window.showMaximized()
    sys.exit(app.exec())
