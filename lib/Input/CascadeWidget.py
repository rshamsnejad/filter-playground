from PyQt6.QtWidgets import (
    QTabWidget,
)
from lib.Engine.CascadeEngine import CascadeEngine
from lib.Engine.BiquadEngine import BiquadEngine
from lib.Input.InputFilterWidget import InputFilterWidget
from lib.Input.InputBodeGraphWidget import InputBodeGraphWidget
from lib.Input.FilterToolbarWidget import FilterToolbarWidget
from lib.Input.CascadeFilterWidget import CascadeFilterWidget
from lib.Input.CascadeToolbarWidget import CascadeToolbarWidget
from lib.Output.OutputBodeGraphWidget import OutputBodeGraphWidget
from lib.Output.OutputWidget import OutputWidget

class CascadeWidget(QTabWidget):
    """
    Qt widget for the the cascade of input filters
    """

    def __init__(self,
        id: int,
        output_widget: OutputWidget,
        initial_amount: int = 2,
        *args, **kwargs
    ) -> None:
        """
        Args:
            output_widget (OutputWidget): The output widget of the main window
            initial_amount (int): The amount to display on init. Defaults to 2
        """

        super().__init__(*args, **kwargs)

        self.id = id
        self.output_widget = output_widget

        if initial_amount <= 0:
            self.initial_amount = 2
            raise ValueError("Input amount should be a positive integer")
        else:
            self.initial_amount = initial_amount

        self.input_filter_widgets = []
        for i in range(self.initial_amount):
            self.add_input_filter_widget(i + 1)

        self.hidden_filters = 0

        self.cascade_filter_widget = CascadeFilterWidget(
            self.input_filter_widgets,
            CascadeEngine(id = self.id),
            CascadeToolbarWidget(self.update_input_filter_amount),
            "Parameters",
            OutputBodeGraphWidget(),
        )
        self.addTab(self.cascade_filter_widget, f"Cascade {chr(ord('A') + self.id)}")

        # Show Bode plot on load
        self.cascade_filter_widget.setCurrentIndex(1)

        self.cascade_filter_widget.cascade_toolbar.field_gain.valueChanged.connect(
            self.output_widget.sum_output_widget.compute_and_update
        )
        self.cascade_filter_widget.cascade_toolbar.field_flip_phase.stateChanged.connect(
            self.output_widget.sum_output_widget.compute_and_update
        )

        currentTab = 1
        for filter_widget in self.input_filter_widgets:
            self.addTab(filter_widget, f"{currentTab}")

            filter_widget.filter_toolbar.filter_type.combo_box.currentTextChanged.connect(self.cascade_filter_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_order.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_frequency.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_gain.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_Q.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_flip_phase.stateChanged.connect(self.cascade_filter_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_passband_ripple.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_stopband_attenuation.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_transband_width.valueChanged.connect(self.cascade_filter_widget.compute_and_update)

            filter_widget.filter_toolbar.filter_type.combo_box.currentTextChanged.connect(self.output_widget.sum_output_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_order.valueChanged.connect(self.output_widget.sum_output_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_frequency.valueChanged.connect(self.output_widget.sum_output_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_gain.valueChanged.connect(self.output_widget.sum_output_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_Q.valueChanged.connect(self.output_widget.sum_output_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_flip_phase.stateChanged.connect(self.output_widget.sum_output_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_passband_ripple.valueChanged.connect(self.output_widget.sum_output_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_stopband_attenuation.valueChanged.connect(self.output_widget.sum_output_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_transband_width.valueChanged.connect(self.output_widget.sum_output_widget.compute_and_update)

            currentTab += 1

    def add_input_filter_widget(self, id: int) -> InputFilterWidget:
        """
        Adds a new input filter to the cascade.

        Args:
            id (int): The display ID of the filter

        Returns:
            InputFilterWidget: The newly created input filter widget
        """

        self.input_filter_widgets.append(
            InputFilterWidget(
                id,
                BiquadEngine(),
                FilterToolbarWidget(id),
                "Parameters",
                InputBodeGraphWidget()
            )
        )

        return self.input_filter_widgets[-1]


    def update_input_filter_amount(self) -> None:
        """
        Qt slot, allows to dynamically update the amount of filter cells
        according to the spinbox in the toolbar.
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
                    input_filter_widget = self.add_input_filter_widget(i)

                    input_filter_widget.filter_toolbar.filter_type.combo_box.currentTextChanged.connect(self.cascade_filter_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_order.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_frequency.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_gain.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_Q.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_flip_phase.stateChanged.connect(self.cascade_filter_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_passband_ripple.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_stopband_attenuation.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_transband_width.valueChanged.connect(self.cascade_filter_widget.compute_and_update)

                    input_filter_widget.filter_toolbar.filter_type.combo_box.currentTextChanged.connect(self.output_widget.sum_output_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_order.valueChanged.connect(self.output_widget.sum_output_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_frequency.valueChanged.connect(self.output_widget.sum_output_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_gain.valueChanged.connect(self.output_widget.sum_output_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_Q.valueChanged.connect(self.output_widget.sum_output_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_flip_phase.stateChanged.connect(self.output_widget.sum_output_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_passband_ripple.valueChanged.connect(self.output_widget.sum_output_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_stopband_attenuation.valueChanged.connect(self.output_widget.sum_output_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_transband_width.valueChanged.connect(self.output_widget.sum_output_widget.compute_and_update)

                    self.addTab(input_filter_widget, f"{i}")
                    widget = input_filter_widget

                # Focus on the newly appeared tab
                #self.setCurrentIndex(i)

                self.output_widget.sum_output_widget.bode_graph.update_axvlines()
                self.cascade_filter_widget.engine.add_engine(widget.engine)
                self.cascade_filter_widget.bode_graph.add_axvline()

        elif new_amount < current_amount:
            # +1 for the cascade tab
            for i in range(new_amount + 1, current_amount + 1):
                self.setTabVisible(i, False)
                self.hidden_filters += 1

                self.output_widget.sum_output_widget.bode_graph.update_axvlines()
                self.cascade_filter_widget.engine.remove_last_engine()
                self.cascade_filter_widget.bode_graph.remove_last_axvline()

        self.cascade_filter_widget.compute_and_update(False)
        self.output_widget.sum_output_widget.compute_and_update()

    def compute_and_update(self, enable_popup: bool = True) -> None:
        """
        Convenience method to wrap computing all the
        filters and updating their graphs in one go
        """

        for widget in self.input_filter_widgets:
            widget.compute_and_update(enable_popup)

        self.cascade_filter_widget.compute_and_update(enable_popup)

    def handle_sample_frequency(self, sample_frequency: str) -> None:
        """
        Convenience Qt slot to trigger all the input engines's same slots
        """

        for widget in self.input_filter_widgets:
            widget.handle_sample_frequency(sample_frequency)

        self.cascade_filter_widget.handle_sample_frequency(sample_frequency)