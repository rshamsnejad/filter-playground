from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QSpinBox,
    QLabel,
    QCheckBox,
    QSpacerItem,
    QSizePolicy,
    QDoubleSpinBox
)

from PyQt6.QtCore import QLocale

from typing import Callable

class CascadeToolbarWidget(QWidget):

    def __init__(self,
        update_callback: Callable,
        *args, **kwargs
    ) -> None:

        super().__init__(*args, **kwargs)

        self.setLayout(QGridLayout())
        spinbox_width = 60
        locale = QLocale("en_US")

        self.label = QLabel("Amount of input filters:")

        self.field_input_amount = QSpinBox()
        self.field_input_amount.setMinimum(1)
        self.field_input_amount.setMaximum(100)
        self.field_input_amount.setValue(2)
        self.field_input_amount.setFixedWidth(spinbox_width)

        self.layout().addWidget(self.label, 0, 0)
        self.layout().addWidget(self.field_input_amount, 0, 1)

        label_gain = QLabel("Gain (dB):")
        self.field_gain = QDoubleSpinBox()
        self.field_gain.setLocale(locale)
        self.field_gain.setMinimum(-100)
        self.field_gain.setMaximum(100)
        self.field_gain.setValue(0)
        self.field_gain.setFixedWidth(spinbox_width)
        self.field_gain.setAccelerated(True)

        self.layout().addWidget(label_gain, 1, 0)
        self.layout().addWidget(self.field_gain, 1, 1)

        label_flip_phase = QLabel("Flip phase:")
        self.field_flip_phase = QCheckBox()
        self.field_flip_phase.setChecked(False)

        self.layout().addWidget(label_flip_phase, 2, 0)
        self.layout().addWidget(self.field_flip_phase, 2, 1)

        self.layout().addItem(
            QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding),
            3, 1, 1, 1
        )

        self.field_input_amount.valueChanged.connect(update_callback)