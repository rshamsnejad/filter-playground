from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QSpinBox,
    QLabel,
    QCheckBox,
    QSpacerItem,
    QSizePolicy,
    QDoubleSpinBox,
    QGroupBox,
    QPushButton
)

from PyQt6.QtCore import QLocale

from typing import Callable

class CascadeToolbarWidget(QWidget):
    """
    Toolbar to display as first tab in a CascadeWidget.
    """

    def __init__(self,
        update_callback: Callable,
        *args, **kwargs
    ) -> None:
        """
        Args:
            update_callback (Callable): The callback to use when changing the input amount
        """

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

        self.parameters_groupbox = QGroupBox("Cascade parameters")
        self.layout().addWidget(self.parameters_groupbox, 1, 0, 1, 2)

        self.parameters_groupbox.setLayout(QGridLayout())

        label_gain = QLabel("Gain (dB):")
        self.field_gain = QDoubleSpinBox()
        self.field_gain.setLocale(locale)
        self.field_gain.setMinimum(-100)
        self.field_gain.setMaximum(100)
        self.field_gain.setValue(0)
        self.field_gain.setFixedWidth(spinbox_width)
        self.field_gain.setAccelerated(True)

        self.parameters_groupbox.layout().addWidget(label_gain, 0, 0)
        self.parameters_groupbox.layout().addWidget(self.field_gain, 0, 1)

        label_flip_phase = QLabel("Flip phase:")
        self.field_flip_phase = QCheckBox()
        self.field_flip_phase.setChecked(False)

        self.parameters_groupbox.layout().addWidget(label_flip_phase, 1, 0)
        self.parameters_groupbox.layout().addWidget(self.field_flip_phase, 1, 1)

        label_delay_samples = QLabel("Delay (samples):")
        self.field_delay_samples = QSpinBox()
        self.field_delay_samples.setMinimum(0)
        self.field_delay_samples.setValue(0)
        self.field_delay_samples.setFixedWidth(spinbox_width)
        self.field_delay_samples.setAccelerated(True)

        self.parameters_groupbox.layout().addWidget(label_delay_samples, 2, 0)
        self.parameters_groupbox.layout().addWidget(self.field_delay_samples, 2, 1)

        self.compute_button = QPushButton("🧠 Compute")

        self.parameters_groupbox.layout().addWidget(self.compute_button, 3, 0, 1, 2)

        self.layout().addItem(
            QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding),
            2, 2, 1, 1
        )

        self.field_input_amount.valueChanged.connect(update_callback)