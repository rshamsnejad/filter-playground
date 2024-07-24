from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout
)
from PyQt6.QtGui import (
    QIcon
)
from lib.InputFilterWidget import InputFilterWidget
from lib.OutputGraphWidget import OutputGraphWidget
from lib.SumEngine import SumEngine


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Filter Playground")
        self.setWindowIcon(QIcon('images/arkamys.jpg'))

        self.setLayout(QGridLayout())

        self.input_filters = [InputFilterWidget(), InputFilterWidget(), InputFilterWidget(), InputFilterWidget()]
        self.output_graph = OutputGraphWidget(SumEngine([filter.graph.engine for filter in self.input_filters]))


        column = 0
        for filter in self.input_filters:
            self.layout().addWidget(filter, 0, column, 1, 1)
            filter.filter_toolbar.filter_type.button_group.buttonToggled.connect(self.output_graph.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_order.textChanged.connect(self.output_graph.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_cutoff.textChanged.connect(self.output_graph.compute_and_update)
            column += 1

        self.layout().addWidget(self.output_graph, 1, 0, 1, -1)

        self.show()
