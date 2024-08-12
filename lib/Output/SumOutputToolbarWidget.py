from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSpinBox,
    QLabel
)
from typing import Callable

class SumOutputToolbarWidget(QWidget):

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self.setLayout(QHBoxLayout())

        self.label = QLabel("Amount of input cascades:")

        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(1)
        self.spinbox.setMaximum(10)
        self.spinbox.setValue(2)
        self.spinbox.setFixedWidth(40)

        self.layout().addWidget(self.label)
        self.layout().addWidget(self.spinbox)
        self.layout().addStretch()

    def set_update_callback(self, update_callback: Callable) -> None:

        self.spinbox.valueChanged.connect(update_callback)