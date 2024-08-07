from PyQt6.QtWidgets import (
    QTabWidget,
)
from lib.Engine.CascadeEngine import CascadeEngine
from lib.Engine.BiquadEngine import BiquadEngine
from lib.Input.InputFilterWidget import InputFilterWidget
from lib.Input.FilterToolbarWidget import FilterToolbarWidget
from lib.Graph.DualGraphWidget import DualGraphWidget
from lib.Output.OutputBodeGraphWidget import OutputBodeGraphWidget
from lib.Output.OutputWidget import OutputWidget


class CascadeWidget(QTabWidget):
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
            self.input_filters.append(InputFilterWidget(i + 1, FilterToolbarWidget(i + 1), "Parameters", BiquadEngine()))

        self.hidden_filters = 0

        self.cascade_widget = DualGraphWidget(OutputBodeGraphWidget())
        self.cascade_widget.set_engine(
            CascadeEngine([filter.engine for filter in self.input_filters])
        )

        self.addTab(self.cascade_widget, "Cascade")

        currentTab = 1
        for filter in self.input_filters:
            self.addTab(filter, f"{currentTab}")
            filter.filter_toolbar.filter_type.combo_box.currentTextChanged.connect(self.output_widget.output_dualgraph.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_order.valueChanged.connect(self.output_widget.output_dualgraph.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_frequency.valueChanged.connect(self.output_widget.output_dualgraph.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_gain.valueChanged.connect(self.output_widget.output_dualgraph.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_Q.valueChanged.connect(self.output_widget.output_dualgraph.compute_and_update)

            filter.filter_toolbar.filter_type.combo_box.currentTextChanged.connect(self.cascade_widget.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_order.valueChanged.connect(self.cascade_widget.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_frequency.valueChanged.connect(self.cascade_widget.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_gain.valueChanged.connect(self.cascade_widget.compute_and_update)
            filter.filter_toolbar.filter_parameters.field_Q.valueChanged.connect(self.cascade_widget.compute_and_update)
            currentTab += 1

    def update_input_filter_amount(self) -> None:
        """
        Qt slot, allows to dynamically update the amount of filter cells
        according to the spinbox in the main window
        """
        spinbox = self.sender()

        # -1 for the cascade tab
        current_amount = self.count() - self.hidden_filters - 1
        new_amount = spinbox.value()

        if new_amount == current_amount:
            return

        if new_amount > current_amount:
            # +1 for the cascade tab
            for i in range(current_amount + 1, new_amount + 1):
                widget = self.widget(i)

                # If a cell was previously added and hidden, simply show it again
                if(widget):
                    self.setTabVisible(i, True)
                    self.hidden_filters -= 1

                # Otherwise create a new one
                else:
                    filter = InputFilterWidget(i)
                    filter.filter_toolbar.filter_type.combo_box.currentTextChanged.connect(self.output_widget.output_dualgraph.compute_and_update)
                    filter.filter_toolbar.filter_parameters.field_order.valueChanged.connect(self.output_widget.output_dualgraph.compute_and_update)
                    filter.filter_toolbar.filter_parameters.field_frequency.valueChanged.connect(self.output_widget.output_dualgraph.compute_and_update)
                    filter.filter_toolbar.filter_parameters.field_gain.valueChanged.connect(self.output_widget.output_dualgraph.compute_and_update)
                    filter.filter_toolbar.filter_parameters.field_Q.valueChanged.connect(self.output_widget.output_dualgraph.compute_and_update)

                    filter.filter_toolbar.filter_type.combo_box.currentTextChanged.connect(self.cascade_widget.compute_and_update)
                    filter.filter_toolbar.filter_parameters.field_order.valueChanged.connect(self.cascade_widget.compute_and_update)
                    filter.filter_toolbar.filter_parameters.field_frequency.valueChanged.connect(self.cascade_widget.compute_and_update)
                    filter.filter_toolbar.filter_parameters.field_gain.valueChanged.connect(self.cascade_widget.compute_and_update)
                    filter.filter_toolbar.filter_parameters.field_Q.valueChanged.connect(self.cascade_widget.compute_and_update)
                    self.addTab(filter, f"{i}")
                    widget = filter

                # Focus on the newly appeared tab
                #self.setCurrentIndex(i)

                self.output_widget.output_dualgraph.engine.add_engine(widget.engine)
                self.output_widget.output_dualgraph.bode_graph.add_axvline()
                self.cascade_widget.engine.add_engine(widget.engine)
                self.cascade_widget.bode_graph.add_axvline()

        elif new_amount < current_amount:
            # +1 for the cascade tab
            for i in range(new_amount + 1, current_amount + 1):
                self.setTabVisible(i, False)
                self.hidden_filters += 1

                self.output_widget.output_dualgraph.engine.remove_last_engine()
                self.output_widget.output_dualgraph.bode_graph.remove_last_axvline()
                self.cascade_widget.engine.remove_last_engine()
                self.cascade_widget.bode_graph.remove_last_axvline()

        self.output_widget.output_dualgraph.compute_and_update()
        self.cascade_widget.compute_and_update()

