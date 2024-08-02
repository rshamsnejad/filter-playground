from PyQt6.QtWidgets import (
    QTabWidget,
)
from lib.InputFilterWidget import InputFilterWidget
from lib.OutputWidget import OutputWidget


class InputWidget(QTabWidget):
    """
    Qt widget for the input filters
    """

    def __init__(self,
        output_widget: OutputWidget,
        initial_amount: int = 2,
        *args, **kwargs
    ) -> None:
        """
        Args:
            output_widget (OutputWidget): The output widget of the main window
        """

        super().__init__(*args, **kwargs)

        self.output_widget = output_widget

        if initial_amount <= 0:
            self.initial_amount = 2
            raise ValueError("Input amount should be a positive integer")
        else:
            self.initial_amount = initial_amount

        self.input_filters = []
        for i in range(self.initial_amount):
            self.input_filters.append(InputFilterWidget(i + 1))

        self.hidden_filters = 0

        currentTab = 1
        for filter in self.input_filters:
            self.addTab(filter, f"{currentTab}")
            filter.filter_toolbar.filter_type.combo_box.currentTextChanged.connect(self.output_widget.output_graph.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_order.valueChanged.connect(self.output_widget.output_graph.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_frequency.valueChanged.connect(self.output_widget.output_graph.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_gain.valueChanged.connect(self.output_widget.output_graph.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_Q.valueChanged.connect(self.output_widget.output_graph.compute_and_update)
            currentTab += 1

    def update_input_filter_amount(self) -> None:
        """
        Qt slot, allows to dynamically update the amount of filter cells
        according to the spinbox in the main window
        """
        spinbox = self.sender()

        current_amount = self.count() - self.hidden_filters
        new_amount = spinbox.value()

        if new_amount == current_amount:
            return

        if new_amount > current_amount:
            for i in range(current_amount, new_amount):
                widget = self.widget(i)

                # If a cell was previously added and hidden, simply show it again
                if(widget):
                    self.setTabVisible(i, True)
                    self.hidden_filters -= 1

                # Otherwise create a new one
                else:
                    filter = InputFilterWidget(i + 1)
                    filter.filter_toolbar.filter_type.combo_box.currentTextChanged.connect(self.output_widget.output_graph.compute_and_update)
                    filter.filter_toolbar.filter_parameters.field_order.valueChanged.connect(self.output_widget.output_graph.compute_and_update)
                    filter.filter_toolbar.filter_parameters.field_frequency.valueChanged.connect(self.output_widget.output_graph.compute_and_update)
                    filter.filter_toolbar.filter_parameters.field_gain.valueChanged.connect(self.output_widget.output_graph.compute_and_update)
                    filter.filter_toolbar.filter_parameters.field_Q.valueChanged.connect(self.output_widget.output_graph.compute_and_update)
                    self.addTab(filter, f"{i + 1}")
                    widget = filter

                self.output_widget.output_graph.engine.add_engine(widget.graph.engine)
                self.output_widget.output_graph.add_axvline()

        elif new_amount < current_amount:
            for i in range(new_amount, current_amount):
                self.setTabVisible(i, False)
                self.hidden_filters += 1

                self.output_widget.output_graph.engine.remove_last_engine()
                self.output_widget.output_graph.remove_last_axvline()

        self.output_widget.output_graph.compute_and_update()

