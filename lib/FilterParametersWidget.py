from PyQt6.QtWidgets import (
    QGroupBox,
    QGridLayout,
    QLabel,
    QSpinBox
)

class FilterParametersWidget(QGroupBox):
    def __init__(self,
        order: int,
        cutoff: float,
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
