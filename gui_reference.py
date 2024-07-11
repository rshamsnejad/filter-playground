import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QLabel,
    QPushButton,
    QVBoxLayout
)
from PyQt6.QtGui import (
    QIcon
)

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Pouet")
        self.setWindowIcon(QIcon('arkamys.jpg'))

        self.button = QPushButton('Cliquouille')
        self.button.clicked.connect(self.button_clicked)

        self.label = QLabel()
        self.line_edit = QLineEdit(textChanged=self.label.setText)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.button)
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)

        self.show()

    def button_clicked(self):
        self.line_edit.setText("")
        self.label.setText("Reset !")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec())