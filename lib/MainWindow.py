from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout
)
from PyQt6.QtGui import (
    QIcon
)
from lib.InputFilterWidget import InputFilterWidget
from lib.GraphWidget import GraphWidget
from lib.SumEngine import SumEngine


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Filter Playground")
        self.setWindowIcon(QIcon('images/arkamys.jpg'))

        self.setLayout(QGridLayout())

        self.input_filters = [InputFilterWidget(), InputFilterWidget()]

        column = 0
        for filter in self.input_filters:
            self.layout().addWidget(filter, 0, column, 1, 1)
            column += 1

        self.output_graph = GraphWidget(SumEngine([filter.graph.engine for filter in self.input_filters]))

        self.layout().addWidget(self.output_graph, 1, 0, 1, -1)

        self.show()
