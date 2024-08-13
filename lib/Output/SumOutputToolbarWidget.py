from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QSpinBox,
    QLabel
)
from typing import Callable

class SumOutputToolbarWidget(QWidget):

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self.setLayout(QGridLayout())

        self.label = QLabel("Amount of input cascades:")

        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(1)
        self.spinbox.setMaximum(10)
        self.spinbox.setValue(2)
        self.spinbox.setFixedWidth(40)

        self.layout().addWidget(self.label, 0, 0)
        self.layout().addWidget(self.spinbox, 0, 1)

        self.layout().addItem(
            QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding),
            1, 1, 1, 1
        )

    def set_update_callback(self, update_callback: Callable) -> None:

        self.spinbox.valueChanged.connect(update_callback)