from PyQt6.QtWidgets import QMainWindow, QToolBar, QComboBox, QLabel
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
            mpls.use("default")
        else:
            self.color_scheme = "dark"
            mpls.use("./lib/custom_dark.mplstyle")

        self.setWindowTitle("Filter Playground")
        self.setWindowIcon(QIcon('images/frequency.png'))

        self.fs_label = QLabel("Sample frequency: ")

        self.fs_combobox = QComboBox()
        self.fs_combobox.addItems([
            "44100",  "48000",
            "88200",  "96000",
            "176400", "192000"
        ])
        self.fs_combobox.setEditable(True)
        self.fs_combobox.setCurrentText("48000")

        self.toolbar = QToolBar()
        self.toolbar.addWidget(self.fs_label)
        self.toolbar.addWidget(self.fs_combobox)
        self.toolbar.setMovable(False)

        self.addToolBar(self.toolbar)

        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

        self.fs_combobox.currentTextChanged.connect(self.main_widget.handle_sample_frequency)

        self.main_widget.compute_and_update(enable_popup=False)

        self.show()