from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QScrollArea
)

from lib.Output.OutputWidget import OutputWidget
from lib.Engine.CascadeEngine import CascadeEngine
from lib.Input.InputWidget import InputWidget

class MainWidget(QWidget):
    """
    Main Qt widget to display in the window
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setLayout(QHBoxLayout())

        self.output_widget = OutputWidget()
        self.input_widget = InputWidget(self.output_widget)

        input_engines = []

        for cascade_widget in self.input_widget.cascade_widgets:
            for filter in cascade_widget.input_filters:
                input_engines.append(filter.engine)

        engine = CascadeEngine()
        engine.set_input_engines(input_engines)
        self.output_widget.output_dualgraph.set_engine(engine)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.input_widget)
        self.scroll_area.setWidgetResizable(True)

        self.layout().addWidget(self.scroll_area)
        self.layout().addWidget(self.output_widget)

