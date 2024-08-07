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

        self.setLayout(QVBoxLayout())

        self.cascade_widgets = []
        
        for i in range(2):
            self.cascade_widgets.append(
                CascadeWidget(self.output_widget, 2)
            )

        for widget in self.cascade_widgets:
            self.layout().addWidget(widget)