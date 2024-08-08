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

        self.input_filter_widgets = []
        for i in range(self.initial_amount):
            self.add_input_filter_widget(i + 1)

        self.hidden_filters = 0

        self.cascade_filter_widget = CascadeFilterWidget(
            self.input_filter_widgets,
            CascadeEngine(),
            CascadeToolbarWidget(self.update_input_filter_amount),
            "Parameters",
            OutputBodeGraphWidget(),
        )
        self.addTab(self.cascade_filter_widget, "Cascade")

        currentTab = 1
        for filter_widget in self.input_filter_widgets:
            self.addTab(filter_widget, f"{currentTab}")

            filter_widget.filter_toolbar.filter_type.combo_box.currentTextChanged.connect(self.cascade_filter_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_order.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_frequency.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_gain.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_Q.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_passband_ripple.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_stopband_attenuation.valueChanged.connect(self.cascade_filter_widget.compute_and_update)

            filter_widget.filter_toolbar.filter_type.combo_box.currentTextChanged.connect(self.output_widget.output_dualgraph.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_order.valueChanged.connect(self.output_widget.output_dualgraph.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_frequency.valueChanged.connect(self.output_widget.output_dualgraph.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_gain.valueChanged.connect(self.output_widget.output_dualgraph.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_Q.valueChanged.connect(self.output_widget.output_dualgraph.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_passband_ripple.valueChanged.connect(self.output_widget.output_dualgraph.compute_and_update)
            filter_widget.filter_toolbar.filter_parameters.field_stopband_attenuation.valueChanged.connect(self.output_widget.output_dualgraph.compute_and_update)

            currentTab += 1

    def add_input_filter_widget(self, id: int) -> InputFilterWidget:

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
                    input_filter_widget = self.add_input_filter_widget(i)

                    input_filter_widget.filter_toolbar.filter_type.combo_box.currentTextChanged.connect(self.cascade_filter_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_order.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_frequency.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_gain.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_Q.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_passband_ripple.valueChanged.connect(self.cascade_filter_widget.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_stopband_attenuation.valueChanged.connect(self.cascade_filter_widget.compute_and_update)

                    input_filter_widget.filter_toolbar.filter_type.combo_box.currentTextChanged.connect(self.output_widget.output_dualgraph.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_order.valueChanged.connect(self.output_widget.output_dualgraph.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_frequency.valueChanged.connect(self.output_widget.output_dualgraph.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_gain.valueChanged.connect(self.output_widget.output_dualgraph.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_Q.valueChanged.connect(self.output_widget.output_dualgraph.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_passband_ripple.valueChanged.connect(self.output_widget.output_dualgraph.compute_and_update)
                    input_filter_widget.filter_toolbar.filter_parameters.field_stopband_attenuation.valueChanged.connect(self.output_widget.output_dualgraph.compute_and_update)

                    self.addTab(input_filter_widget, f"{i}")
                    widget = input_filter_widget

                # Focus on the newly appeared tab
                #self.setCurrentIndex(i)

                self.output_widget.output_dualgraph.bode_graph.add_axvline()
                self.cascade_filter_widget.engine.add_engine(widget.engine)
                self.cascade_filter_widget.bode_graph.add_axvline()

        elif new_amount < current_amount:
            # +1 for the cascade tab
            for i in range(new_amount + 1, current_amount + 1):
                self.setTabVisible(i, False)
                self.hidden_filters += 1

                self.output_widget.output_dualgraph.bode_graph.remove_last_axvline()
                self.cascade_filter_widget.engine.remove_last_engine()
                self.cascade_filter_widget.bode_graph.remove_last_axvline()

        self.cascade_filter_widget.compute_and_update()
        self.output_widget.output_dualgraph.compute_and_update()

