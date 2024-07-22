import logging
from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QGroupBox,
    QRadioButton,
    QLineEdit,
    QLabel
)
from PyQt6.QtGui import (
    QIcon
)
from lib.FilterEngine import FilterEngine


class SingleFilterWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__layout = QGridLayout()
        self.setLayout(self.__layout)

        self.__filterengine = FilterEngine(self.__layout)

        self.init_type_box()
        self.init_order_field()
        self.init_cutoff_field()

        self.show()

    def init_type_box(self):
        button_box = QVBoxLayout()
        types = ["Highpass", "Lowpass"]#, "Bandpass", "Bandstop"]
        radio_buttons = []
        for type in types:
            radio_buttons.append(QRadioButton(type, self))
            radio_buttons[-1].toggled.connect(self.handle_type)

            button_box.addWidget(radio_buttons[-1])

        radio_buttons[0].setChecked(True)

        button_group = QGroupBox("Filter type")
        button_group.setLayout(button_box)

        self.__layout.addWidget(button_group, 0, 0, 1, 1)

    def init_order_field(self):
        label_order = QLabel("Filter order:")

        field_order = QLineEdit(str(self.__filterengine.get_order()), self)
        field_order.placeholderText = "Order"
        field_order.maxLength = 3
        field_order.textChanged.connect(self.handle_order)

        self.__layout.addWidget(label_order, 0, 1, 1, 1)
        self.__layout.addWidget(field_order, 0, 2, 1, 1)

    def init_cutoff_field(self):
        label_cutoff = QLabel("Cutoff frequency:")

        field_cutoff = QLineEdit(str(self.__filterengine.get_cutoff()), self)
        field_cutoff.placeholderText = "Cutoff"
        field_cutoff.maxLength = 5
        field_cutoff.textChanged.connect(self.handle_cutoff)

        self.__layout.addWidget(label_cutoff, 1, 1, 1, 1)
        self.__layout.addWidget(field_cutoff, 1, 2, 1, 1)


    def handle_type(self):
        rb = self.sender()

        self.__filterengine.set_filtertype(rb.text())
        self.__filterengine.update_filter()

    def handle_order(self):
        rb = self.sender()

        try:
            self.__filterengine.set_order(int(rb.text() or 1))
        except ValueError as e:
            logging.warning(e)

        self.__filterengine.update_filter()

    def handle_cutoff(self):
        rb = self.sender()

        try:
            self.__filterengine.set_cutoff(int(rb.text() or 1000))
        except ValueError as e:
            logging.warning(e)

        self.__filterengine.update_filter()

