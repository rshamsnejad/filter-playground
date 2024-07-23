from PyQt6.QtWidgets import (
    QGroupBox,
    QGridLayout,
    QLabel,
    QLineEdit
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
        self.field_order = QLineEdit(str(order), self)
        self.field_order.placeholderText = "Order"
        self.field_order.maxLength = 3

        self.layout().addWidget(label_order, 0, 0, 1, 1)
        self.layout().addWidget(self.field_order, 0, 1, 1, 1)

        label_cutoff = QLabel("Cutoff frequency:")
        field_cutoff = QLineEdit(str(cutoff), self)
        field_cutoff.placeholderText = "Cutoff"
        field_cutoff.maxLength = 5

        self.layout().addWidget(label_cutoff, 1, 0, 1, 1)
        self.layout().addWidget(field_cutoff, 1, 1, 1, 1)
