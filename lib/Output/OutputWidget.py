from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout
)

from lib.Graph.DualGraphWidget import DualGraphWidget
from lib.Output.SumOutputBodeGraphWidget import SumOutputBodeGraphWidget


class OutputWidget(QWidget):
    """
    Qt widget for the output graph
    """

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self.setLayout(QHBoxLayout())

        self.output_dualgraph = DualGraphWidget(SumOutputBodeGraphWidget())

        self.layout().addWidget(self.output_dualgraph)
