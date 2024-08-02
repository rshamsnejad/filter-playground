from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
)
from lib.Input.FilterTypeWidget import FilterTypeWidget
from lib.Input.FilterParametersWidget import FilterParametersWidget

class FilterToolbarWidget(QWidget):
    """
    Qt widget to set a cell's filter type and parameters
    """

    def __init__(self, id: int, *args, **kwargs) -> None:
        """
        Args:
            id (int): The number of the filter to display
        """

        super().__init__(*args, **kwargs)

        self.id = id

        self.setLayout(QHBoxLayout())

        self.filter_type = FilterTypeWidget(self.id)
        self.filter_parameters = FilterParametersWidget(2, 1000, 0, 0.71)

        self.layout().addWidget(self.filter_type)
        self.layout().addWidget(self.filter_parameters)

