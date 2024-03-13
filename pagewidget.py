from PySide6 import QtCore, QtWidgets, QtWebEngineWidgets, QtGui, QtWebEngineCore
from plotly.graph_objects import Figure
from pandas import DataFrame


class PageWidget(QtWidgets.QWidget):
    def __init__(self, df: DataFrame, fig: Figure, sequence: list[int], total_time: int, downtime: int):
        super().__init__()
        self.dataframe = df
        self.fig = fig
        self.sequence = sequence
        self.downtime = downtime
        self.total_time = total_time

        v_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(v_layout)

        self.browser = QtWebEngineWidgets.QWebEngineView()
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
        v_layout.addWidget(self.browser)

        sequence_text = "–".join(map(lambda x: str(x + 1), sequence))
        labels_size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                                   QtWidgets.QSizePolicy.Policy.Maximum)
        labels_font = QtGui.QFont(["Open Sans", "verdana", "arial", "sans-serif"], 11, 8)

        self.sequence_label = QtWidgets.QLabel(f"Последовательность: {sequence_text}")
        self.sequence_label.setSizePolicy(labels_size_policy)
        self.sequence_label.setFont(labels_font)
        v_layout.addWidget(self.sequence_label, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.time_label = QtWidgets.QLabel(f"Время обработки: {total_time}\t Время простоя: {downtime}")
        self.time_label.setSizePolicy(labels_size_policy)
        self.time_label.setFont(labels_font)
        v_layout.addWidget(self.time_label, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

    def save_diagram(self, filename):
        self.browser.page().save(filename,
                                 QtWebEngineCore.QWebEngineDownloadRequest.SavePageFormat.SingleHtmlSaveFormat)

    def save_dataframe(self, filename):
        self.dataframe.to_csv(filename)
