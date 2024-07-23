from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout
)
from PyQt6.QtGui import (
    QIcon
)
from lib.InputFilterWidget import InputFilterWidget


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Filter Playground")
        self.setWindowIcon(QIcon('images/arkamys.jpg'))

        self.__layout = QGridLayout()
        self.setLayout(self.__layout)

        self.__filters = [InputFilterWidget(), InputFilterWidget()]

        column = 0
        for filter in self.__filters:
            self.__layout.addWidget(filter, 0, column, 1, 1)
            column += 1

        self.show()
