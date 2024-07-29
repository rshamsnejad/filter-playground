from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout
)
from lib.OutputGraphWidget import OutputGraphWidget


class OutputWidget(QWidget):
    """
    Qt widget for the output graph
    """

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self.setLayout(QHBoxLayout())

        self.output_graph = OutputGraphWidget()

        self.layout().addWidget(self.output_graph)
