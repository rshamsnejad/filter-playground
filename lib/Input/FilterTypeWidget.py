from PyQt6.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
    QComboBox
)

class FilterTypeWidget(QGroupBox):
    """
    Qt widget for the selection of the filter type
    """

    def __init__(self,
        id: int,
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
        """
        Args:
            id (int): The number of the filter to display
            types (list[str], optional):
                The list to display in the drop-down list.
                Defaults to [ "Highpass", "Lowpass", "Allpass", "Peak", "Highshelf", "Lowshelf" ].
        """

        if id <= 0:
            self.id = 1
            raise ValueError("ID must be a positive integer")
        else:
            self.id = id

        super().__init__(*args, **kwargs)

        self.setTitle("Filter type")
        self.setLayout(QVBoxLayout())

        self.types = types

        self.combo_box = QComboBox()
        self.combo_box.addItems(self.types)

        self.layout().addWidget(self.combo_box)