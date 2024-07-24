from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout
)
from lib.InputFilterWidget import InputFilterWidget
from lib.OutputGraphWidget import OutputGraphWidget
from lib.SumEngine import SumEngine


class MainWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setLayout(QGridLayout())

        self.input_filters = [InputFilterWidget(), InputFilterWidget()]
        self.output_graph = OutputGraphWidget(SumEngine([filter.graph.engine for filter in self.input_filters]))

        self.hidden_filters = 0

        column = 0
        for filter in self.input_filters:
            self.layout().addWidget(filter, 0, column, 1, 1)
            filter.filter_toolbar.filter_type.button_group.buttonToggled.connect(self.output_graph.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_order.textChanged.connect(self.output_graph.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_cutoff.textChanged.connect(self.output_graph.compute_and_update)
            column += 1

        self.layout().addWidget(self.output_graph, 1, 0, 1, -1)

    def update_input_filter_amount(self) -> None:
        spinbox = self.sender()

        current_amount = self.layout().columnCount() - self.hidden_filters
        new_amount = spinbox.value()

        if new_amount == current_amount:
            return
        if new_amount > current_amount:
            for i in range(current_amount, new_amount):
                item = self.layout().itemAtPosition(0, i)
                if(item):
                    item.widget().show()
                    self.hidden_filters -= 1
                else:
                    self.layout().addWidget(InputFilterWidget(), 0, i, 1, 1)
        elif new_amount < current_amount:
            for i in range(new_amount, current_amount):
                self.layout().itemAtPosition(0, i).widget().hide()
                self.hidden_filters += 1

