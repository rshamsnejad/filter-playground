import logging

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QScrollArea,
    QMessageBox
)

from lib.Output.OutputWidget import OutputWidget
from lib.Engine.SumEngine import SumEngine
from lib.Input.InputWidget import InputWidget

class MainWidget(QWidget):
    """
    Main Qt widget to display in the window
    """

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self.setLayout(QHBoxLayout())

        self.output_widget = OutputWidget()
        # Hide unused pole-zero map tab
        self.output_widget.sum_output_widget.setTabVisible(2, False)
        self.input_widget = InputWidget(self.output_widget)

        input_engines = []

        for cascade_widget in self.input_widget.cascade_widgets:
            input_engines.append(cascade_widget.cascade_filter_widget.engine)

        engine = SumEngine()
        engine.set_input_engines(input_engines)
        self.output_widget.sum_output_widget.set_engine(engine)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.input_widget)
        self.scroll_area.setWidgetResizable(True)

        self.layout().addWidget(self.scroll_area)
        self.layout().addWidget(self.output_widget)

        self.popup = QMessageBox()
        self.popup.setWindowTitle("Invalid data")

    def compute_and_update(self) -> None:
        """
        Convenience method to wrap computing all the
        data and updating all the graph in one go
        """

        self.input_widget.compute_and_update()
        self.output_widget.compute_and_update()

    def handle_sample_frequency(self, sample_frequency: str) -> None:
        """
        Convenience Qt slot to trigger all the engines's same slots
        """

        try:
            self.input_widget.handle_sample_frequency(sample_frequency)
            self.output_widget.handle_sample_frequency(sample_frequency)
        except ValueError as e:
            logging.warning(e)
            self.popup.setText(str(e))
            self.popup.exec()