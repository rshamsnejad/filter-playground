from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel
)

class CascadeToolbarWidget(QWidget):

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self.setLayout(QHBoxLayout())

        self.layout().addWidget(QLabel("Toustee"))

