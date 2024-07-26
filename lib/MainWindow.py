from PyQt6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QSpinBox,
    QLabel
)
from PyQt6.QtGui import (
    QIcon
)
from lib.MainWidget import MainWidget

class MainWindow(QMainWindow):
    """
    Base Qt window to display in main
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Filter Playground")
        self.setWindowIcon(QIcon('images/frequency.png'))

        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(2)
        self.spinbox.setMaximum(10)
        self.spinbox.setValue(2)
        self.spinbox.setFixedWidth(70)
        self.spinbox.valueChanged.connect(self.main_widget.update_input_filter_amount)

        self.toolbar = QToolBar('Main toolbar')
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)
        self.toolbar.addWidget(QLabel("Amount of input filters:"))
        self.toolbar.addWidget(self.spinbox)

        self.addToolBar(self.toolbar)

        self.show()