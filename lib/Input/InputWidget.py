from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout
)

from lib.Input.CascadeWidget import CascadeWidget
from lib.Output.OutputWidget import OutputWidget

class InputWidget(QWidget):

    def __init__(self,
        output_widget: OutputWidget,
        *args, **kwargs
        ) -> None:

        super().__init__(*args, **kwargs)

        self.output_widget = output_widget
        self.output_widget.sum_output_widget.sum_toolbar.set_update_callback(self.update_input_cascade_amount)

        self.setLayout(QVBoxLayout())

        self.cascade_widgets = []

        for i in range(2):
            self.add_cascade_widget(i + 1)

        self.hidden_cascades = 0

    def add_cascade_widget(self, id: int) -> CascadeWidget:

            self.cascade_widgets.append(
                CascadeWidget(id, self.output_widget, 2)
            )

            self.layout().addWidget(self.cascade_widgets[-1])

            return self.cascade_widgets[-1]

    def update_input_cascade_amount(self) -> None:
        """
        Qt slot, allows to dynamically update the amount of
        cascade sections according to the spinbox in the output widget
        """

        spinbox = self.sender()

        current_amount = self.layout().count() - self.hidden_cascades
        new_amount = spinbox.value()

        if new_amount == current_amount:
            return

        if new_amount > current_amount:
            for i in range(current_amount, new_amount):
                item = self.layout().itemAt(i)

                # If a cascade was previously added and hidden, simply show it again
                if(item):
                    widget = item.widget()
                    widget.show()
                    self.hidden_cascades -= 1

                # Otherwise create a new one
                else:
                    widget = self.add_cascade_widget(i + 1)

                self.output_widget.sum_output_widget.engine.add_engine(widget.cascade_filter_widget.engine)
                self.output_widget.sum_output_widget.bode_graph.update_axvlines()

        elif new_amount < current_amount:
            for i in range(new_amount, current_amount):
                widget = self.layout().itemAt(i).widget()
                widget.hide()

                self.hidden_cascades += 1

                self.output_widget.sum_output_widget.engine.remove_last_engine()

                self.output_widget.sum_output_widget.bode_graph.update_axvlines()

        self.output_widget.sum_output_widget.compute_and_update()

