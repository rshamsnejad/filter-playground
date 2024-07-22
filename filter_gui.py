import sys
from PyQt6.QtWidgets import QApplication
from lib.SingleFilterWidget import SingleFilterWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = SingleFilterWidget()

    sys.exit(app.exec())