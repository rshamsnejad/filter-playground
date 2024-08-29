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
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Pouet")
        self.setWindowIcon(QIcon('arkamys.jpg'))

        self.button = QPushButton('Cliquouille')
        self.button.clicked.connect(self.button_clicked)

        self.label = QLabel()
        self.line_edit = QLineEdit(
            clearButtonEnabled=True,
            placeholderText="Write here",
            textChanged=self.label.setText
        )

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addStretch()
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addStretch()

        self.show()

    def button_clicked(self) -> None:
        self.line_edit.clear()
        self.label.setText("Reset !")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec())