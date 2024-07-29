from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea
)

from lib.InputWidget import InputWidget
from lib.OutputWidget import OutputWidget
from lib.SumEngine import SumEngine

class MainWidget(QWidget):
    """
    Main Qt widget to display in the window
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setLayout(QVBoxLayout())

        self.output_widget = OutputWidget()
        self.input_widget = InputWidget(self.output_widget)
        self.output_widget.output_graph.set_engine(
            SumEngine([filter.graph.engine for filter in self.input_widget.input_filters])
        )

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.input_widget)
        self.scroll_area.setWidgetResizable(True)

        self.layout().addWidget(self.scroll_area)
        self.layout().addWidget(self.output_widget)

