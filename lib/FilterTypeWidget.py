from PyQt6.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
    QButtonGroup,
    QRadioButton
)

class FilterTypeWidget(QGroupBox):
    def __init__(self,
        types: list[str] = ["Highpass", "Lowpass", "Allpass"],
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self.setTitle("Filter type")
        self.setLayout(QVBoxLayout())

        self.types = types
        self.button_group = QButtonGroup()

        for type in self.types:
            self.button_group.addButton(QRadioButton(type, self))
            self.layout().addWidget(self.button_group.buttons()[-1])

        self.button_group.buttons()[0].setChecked(True)
