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
