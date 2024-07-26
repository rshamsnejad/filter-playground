from PyQt6.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
    QComboBox
)

class FilterTypeWidget(QGroupBox):
    def __init__(self,
        types: list[str] = [
            "Highpass",
            "Lowpass",
            "Allpass",
            "Peak",
            "Highshelf",
            "Lowshelf"
        ],
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self.setTitle("Filter type")
        self.setLayout(QVBoxLayout())

        self.types = types

        self.combo_box = QComboBox()
        self.combo_box.addItems(self.types)

        self.layout().addWidget(self.combo_box)