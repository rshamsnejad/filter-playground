from PyQt6.QtWidgets import (
    QSplitter
)
from PyQt6.QtCore import Qt

from lib.Input.CascadeWidget import CascadeWidget
from lib.Output.OutputWidget import OutputWidget

class InputWidget(QSplitter):
    """
    Qt widget for the left section of the main window
    that contains the inputs
    """

    def __init__(self,
        output_widget: OutputWidget,
        *args, **kwargs
    ) -> None:
        """
        Args:
            output_widget (OutputWidget): The output widget of the main window
        """

        super().__init__(*args, **kwargs)

        self.setOrientation(Qt.Orientation.Vertical)
        self.setOpaqueResize(False)

        self.output_widget = output_widget
        self.output_widget.sum_output_widget.sum_toolbar.set_update_callback(self.update_input_cascade_amount)

        self.cascade_widgets = []

        for i in range(2):
            self.add_cascade_widget(i)

        self.hidden_cascades = 0

    def add_cascade_widget(self, id: int) -> CascadeWidget:
        """
        Adds a new input cascade widget

        Args:
            id (int): The display ID of the cascade

        Returns:
            CascadeWidget: The newly added cascade widget
        """

        self.cascade_widgets.append(
            CascadeWidget(id, self.output_widget, 2)
        )

        self.addWidget(self.cascade_widgets[-1])

        self.cascade_widgets[-1].compute_and_update()

        return self.cascade_widgets[-1]

    def update_input_cascade_amount(self) -> None:
        """
        Qt slot, allows to dynamically update the amount of
        cascade sections according to the spinbox in the output widget
        """

        spinbox = self.sender()

        current_amount = self.count() - self.hidden_cascades
        new_amount = spinbox.value()

        if new_amount == current_amount:
            return

        if new_amount > current_amount:
            for i in range(current_amount, new_amount):
                widget = self.widget(i)

                # If a cascade was previously added and hidden, simply show it again
                if(widget):
                    widget.show()
                    self.hidden_cascades -= 1

                # Otherwise create a new one
                else:
                    widget = self.add_cascade_widget(i)

                self.output_widget.sum_output_widget.engine.add_engine(widget.cascade_filter_widget.engine)
                self.output_widget.sum_output_widget.bode_graph.update_axvlines()

        elif new_amount < current_amount:
            for i in range(new_amount, current_amount):
                widget = self.widget(i)
                widget.hide()

                self.hidden_cascades += 1

                self.output_widget.sum_output_widget.engine.remove_last_engine()

                self.output_widget.sum_output_widget.bode_graph.update_axvlines()

        self.output_widget.sum_output_widget.compute_and_update()

    def compute_and_update(self) -> None:
        """
        Convenience method to wrap computing all the
        cascades and filters and updating their graphs in one go
        """

        for widget in self.cascade_widgets:
            widget.compute_and_update()

    def handle_sample_frequency(self, sample_frequency: str) -> None:
        """
        Convenience Qt slot to trigger all the input engines's same slots
        """

        for widget in self.cascade_widgets:
            widget.handle_sample_frequency(sample_frequency)
