import sys
from PyQt6.QtWidgets import QApplication
from lib.MainWidget import MainWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWidget()

    sys.exit(app.exec())