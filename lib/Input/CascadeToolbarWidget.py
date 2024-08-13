from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QSpinBox,
    QLabel,
    QCheckBox,
    # QSpacerItem
)
from typing import Callable

class CascadeToolbarWidget(QWidget):

    def __init__(self,
        update_callback: Callable,
        *args, **kwargs
    ) -> None:

        super().__init__(*args, **kwargs)

        self.setLayout(QGridLayout())

        self.label = QLabel("Amount of input filters:")

        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(1)
        self.spinbox.setMaximum(100)
        self.spinbox.setValue(2)
        self.spinbox.setFixedWidth(40)

        self.layout().addWidget(self.label, 0, 0, 1, 1)
        self.layout().addWidget(self.spinbox, 0, 1, 1, 1)
        # self.layout().addItem(QSpacerItem(1, 1), 0, 2, 1, 1)

        label_flip_phase = QLabel("Flip phase:")
        self.field_flip_phase = QCheckBox()
        self.field_flip_phase.setChecked(False)

        self.layout().addWidget(label_flip_phase, 1, 0, 1, 1)
        self.layout().addWidget(self.field_flip_phase, 1, 1, 1, 1)
        # self.layout().addItem(QSpacerItem(1, 1), 1, 2, 1, 1)


        self.spinbox.valueChanged.connect(update_callback)