import sys
from PyQt6.QtWidgets import QApplication
from lib.SingleFilterWidget import SingleFilterWidget
from lib.MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec())