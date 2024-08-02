from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout
)

from lib.DualGraphWidget import DualGraphWidget
from lib.OutputBodeGraphWidget import OutputBodeGraphWidget


class OutputWidget(QWidget):
    """
    Qt widget for the output graph
    """

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self.setLayout(QHBoxLayout())

        self.output_dualgraph = DualGraphWidget(OutputBodeGraphWidget())

        self.layout().addWidget(self.output_dualgraph)
