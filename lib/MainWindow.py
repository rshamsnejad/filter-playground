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
        self.output_graph = GraphWidget(SumEngine([filter.graph.engine for filter in self.input_filters]))


        column = 0
        for filter in self.input_filters:
            self.layout().addWidget(filter, 0, column, 1, 1)
            for button in filter.filter_toolbar.filter_type.radio_buttons:
                button.toggled.connect(self.output_graph.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_order.textChanged.connect(self.output_graph.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_cutoff.textChanged.connect(self.output_graph.compute_and_update)
            column += 1



        self.layout().addWidget(self.output_graph, 1, 0, 1, -1)

        self.show()
