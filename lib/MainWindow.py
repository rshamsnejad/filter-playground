from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout
)
from PyQt6.QtGui import (
    QIcon
)
from lib.SingleFilterWidget import SingleFilterWidget


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Filter Playground")
        self.setWindowIcon(QIcon('images/arkamys.jpg'))

        self.__layout = QHBoxLayout()
        self.setLayout(self.__layout)

        self.__filters = [SingleFilterWidget(), SingleFilterWidget()]

        for filter in self.__filters:
            self.__layout.addWidget(filter)

        self.show()
