from PyQt6.QtWidgets import (
    QMainWindow
)
from PyQt6.QtGui import (
    QIcon
)
from lib.MainWidget import MainWidget

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Filter Playground")
        self.setWindowIcon(QIcon('images/frequency.png'))

        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

        self.show()