from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout
)

from lib.Output.SumOutputWidget import SumOutputWidget
from lib.Output.SumOutputBodeGraphWidget import SumOutputBodeGraphWidget
from lib.Output.SumOutputToolbarWidget import SumOutputToolbarWidget


class OutputWidget(QWidget):
    """
    Qt widget for the right section of the main window
    that contains the output sum
    """

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self.setLayout(QHBoxLayout())

        self.sum_output_widget = SumOutputWidget(SumOutputToolbarWidget(), "Configuration", SumOutputBodeGraphWidget())

        self.layout().addWidget(self.sum_output_widget)

    def compute_and_update(self) -> None:
        """
        Convenience method to wrap computing the output
        and updating its graph in one go
        """

        self.sum_output_widget.compute_and_update()

    def handle_sample_frequency(self, sample_frequency: str) -> None:
        """
        Convenience Qt slot to trigger all the engines's same slots
        """

        self.sum_output_widget.handle_sample_frequency(sample_frequency)
