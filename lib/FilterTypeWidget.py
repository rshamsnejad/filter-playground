
from PyQt6.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
    QRadioButton
)

class FilterTypeWidget(QGroupBox):
    def __init__(self,
        types: list[str] = ["Highpass", "Lowpass"],
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self.setTitle("Filter type")
        self.setLayout(QVBoxLayout())

        self.types = types
        self.radio_buttons = []

        for type in self.types:
            self.radio_buttons.append(QRadioButton(type, self))
            self.layout().addWidget(self.radio_buttons[-1])

        self.radio_buttons[0].setChecked(True)
