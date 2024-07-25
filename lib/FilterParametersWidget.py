from PyQt6.QtWidgets import (
    QGroupBox,
    QGridLayout,
    QLabel,
    QSpinBox,
    QDoubleSpinBox
)

class FilterParametersWidget(QGroupBox):
    def __init__(self,
        order: int,
        cutoff: float,
        gain: float,
        Q: float,
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self.setTitle("Filter parameters")
        self.setLayout(QGridLayout())

        label_order = QLabel("Filter order:")
        self.field_order = QSpinBox()
        self.field_order.setMinimum(1)
        self.field_order.setMaximum(10)
        self.field_order.setValue(order)

        self.layout().addWidget(label_order, 0, 0, 1, 1)
        self.layout().addWidget(self.field_order, 0, 1, 1, 1)

        label_cutoff = QLabel("Cutoff frequency:")
        self.field_cutoff = QSpinBox()
        self.field_cutoff.setMinimum(1)
        self.field_cutoff.setMaximum(100000)
        self.field_cutoff.setValue(cutoff)

        self.layout().addWidget(label_cutoff, 1, 0, 1, 1)
        self.layout().addWidget(self.field_cutoff, 1, 1, 1, 1)

        label_gain = QLabel("Gain (dB):")
        self.field_gain = QDoubleSpinBox()
        self.field_gain.setMinimum(-100)
        self.field_gain.setMaximum(100)
        self.field_gain.setValue(gain)

        self.layout().addWidget(label_gain, 0, 2, 1, 1)
        self.layout().addWidget(self.field_gain, 0, 3, 1, 1)

        label_Q = QLabel("Q:")
        self.field_Q = QDoubleSpinBox()
        self.field_Q.setMinimum(0)
        self.field_Q.setMaximum(100)
        self.field_Q.setValue(Q)

        self.layout().addWidget(label_Q, 1, 2, 1, 1)
        self.layout().addWidget(self.field_Q, 1, 3, 1, 1)