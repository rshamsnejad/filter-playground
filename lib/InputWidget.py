from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
)
from lib.InputFilterWidget import InputFilterWidget
from lib.OutputWidget import OutputWidget


class InputWidget(QWidget):
    """
    Qt widget for the input filters
    """

    def __init__(self, output_widget: OutputWidget, *args, **kwargs) -> None:
        """
        Args:
            output_widget (OutputWidget): The output widget of the main window
        """

        super().__init__(*args, **kwargs)

        self.output_widget = output_widget

        self.setLayout(QHBoxLayout())

        self.input_filters = [InputFilterWidget(), InputFilterWidget()]

        self.hidden_filters = 0

        column = 0
        for filter in self.input_filters:
            self.layout().addWidget(filter)
            filter.filter_toolbar.filter_type.combo_box.currentTextChanged.connect(self.output_widget.output_graph.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_order.valueChanged.connect(self.output_widget.output_graph.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_frequency.valueChanged.connect(self.output_widget.output_graph.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_gain.valueChanged.connect(self.output_widget.output_graph.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_Q.valueChanged.connect(self.output_widget.output_graph.compute_and_update)
            column += 1

    def update_input_filter_amount(self) -> None:
        """
        Qt slot, allows to dynamically update the amount of filter cells
        according to the spinbox in the main window
        """
        spinbox = self.sender()

        current_amount = self.layout().count() - self.hidden_filters
        new_amount = spinbox.value()

        if new_amount == current_amount:
            return

        if new_amount > current_amount:
            for i in range(current_amount, new_amount):
                item = self.layout().itemAt(i)

                # If a cell was previously added and hidden, simply show it again
                if(item):
                    item.widget().show()
                    self.hidden_filters -= 1

                # Otherwise create a new one
                else:
                    filter = InputFilterWidget()
                    filter.filter_toolbar.filter_type.combo_box.currentTextChanged.connect(self.output_widget.output_graph.compute_and_update)
                    filter.filter_toolbar.filter_parameters.field_order.valueChanged.connect(self.output_widget.output_graph.compute_and_update)
                    filter.filter_toolbar.filter_parameters.field_frequency.valueChanged.connect(self.output_widget.output_graph.compute_and_update)
                    filter.filter_toolbar.filter_parameters.field_gain.valueChanged.connect(self.output_widget.output_graph.compute_and_update)
                    filter.filter_toolbar.filter_parameters.field_Q.valueChanged.connect(self.output_widget.output_graph.compute_and_update)
                    self.layout().addWidget(filter)

                self.output_widget.output_graph.engine.add_engine(self.layout().itemAt(i).widget().graph.engine)
                self.output_widget.output_graph.add_axvline()

        elif new_amount < current_amount:
            for i in range(new_amount, current_amount):
                self.layout().itemAt(i).widget().hide()
                self.hidden_filters += 1

                self.output_widget.output_graph.engine.remove_last_engine()
                self.output_widget.output_graph.remove_last_axvline()

        self.output_widget.output_graph.compute_and_update()

