from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
)
from lib.FilterTypeWidget import FilterTypeWidget
from lib.FilterParametersWidget import FilterParametersWidget

class FilterToolbarWidget(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setLayout(QHBoxLayout())

        self.layout().addWidget(FilterTypeWidget())
        self.layout().addWidget(FilterParametersWidget(3, 300))

