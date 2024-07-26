from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
)
from lib.FilterTypeWidget import FilterTypeWidget
from lib.FilterParametersWidget import FilterParametersWidget

class FilterToolbarWidget(QWidget):
    """
    Qt widget to set a cell's filter type and parameters
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setLayout(QHBoxLayout())

        self.filter_type = FilterTypeWidget()
        self.filter_parameters = FilterParametersWidget(2, 1000, 0, 0.71)

        self.layout().addWidget(self.filter_type)
        self.layout().addWidget(self.filter_parameters)

