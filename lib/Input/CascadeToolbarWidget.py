from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSpinBox,
    QLabel
)
from typing import Callable

class CascadeToolbarWidget(QWidget):

    def __init__(self,
        update_callback: Callable,
        *args, **kwargs
    ) -> None:

        super().__init__(*args, **kwargs)

        self.setLayout(QHBoxLayout())

        self.label = QLabel("Amount of input filters:")

        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(1)
        self.spinbox.setMaximum(100)
        self.spinbox.setValue(2)
        self.spinbox.setFixedWidth(40)

        self.layout().addWidget(self.label)
        self.layout().addWidget(self.spinbox)
        self.layout().addStretch()

        self.spinbox.valueChanged.connect(update_callback)