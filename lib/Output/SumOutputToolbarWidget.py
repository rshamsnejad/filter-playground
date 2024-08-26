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
    """
    Qt widget to display as the first tab of the output section
    """

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self.setLayout(QGridLayout())

        self.label = QLabel("Amount of input cascades:")

        self.cascade_amount_spinbox = QSpinBox()
        self.cascade_amount_spinbox.setMinimum(1)
        self.cascade_amount_spinbox.setMaximum(10)
        self.cascade_amount_spinbox.setValue(2)
        self.cascade_amount_spinbox.setFixedWidth(40)

        self.layout().addWidget(self.label, 0, 0)
        self.layout().addWidget(self.cascade_amount_spinbox, 0, 1)

        self.layout().addItem(
            QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding),
            1, 1, 1, 1
        )

    def set_update_callback(self, update_callback: Callable) -> None:
        """
        Defines the callback to use when updating the input cascade amount.

        Args:
            update_callback (Callable): The callback to be used
        """

        self.cascade_amount_spinbox.valueChanged.connect(update_callback)