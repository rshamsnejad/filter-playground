from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtCore import Qt
from lib.MainWidget import MainWidget

import matplotlib.style as mpls

class MainWindow(QMainWindow):
    """
    Base Qt window to display in main
    """

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        # Detecting the current color scheme for matplotlib theming
        if QGuiApplication.styleHints().colorScheme() == Qt.ColorScheme.Light:
            self.color_scheme = "light"
        else:
            self.color_scheme = "dark"
            mpls.use("./lib/custom_dark.mplstyle")

        self.setWindowTitle("Filter Playground")
        self.setWindowIcon(QIcon('images/frequency.png'))

        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

        self.show()