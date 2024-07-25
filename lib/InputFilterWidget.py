import logging
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QAbstractButton
)
from lib.FilterToolbarWidget import FilterToolbarWidget
from lib.InputGraphWidget import InputGraphWidget
from lib.BiquadEngine import BiquadEngine

class InputFilterWidget(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setLayout(QVBoxLayout())

        self.graph = InputGraphWidget(BiquadEngine())
        self.filter_toolbar = FilterToolbarWidget()

        self.filter_toolbar.filter_type.button_group.buttonToggled.connect(self.handle_type)
        self.filter_toolbar.filter_parameters.field_order.textChanged.connect(self.handle_order)
        self.filter_toolbar.filter_parameters.field_cutoff.textChanged.connect(self.handle_cutoff)

        self.layout().addWidget(self.filter_toolbar)
        self.layout().addWidget(self.graph)

    def handle_type(self, button: QAbstractButton):
        try:
            self.graph.engine.set_filtertype(button.text() or 'highpass')
        except ValueError as e:
            logging.warning(e)

        self.graph.engine.compute()
        self.graph.update_graph()

    def handle_order(self):
        rb = self.sender()

        try:
            self.graph.engine.set_order(int(rb.text() or 1))
        except ValueError as e:
            logging.warning(e)

        self.graph.engine.compute()
        self.graph.update_graph()

    def handle_cutoff(self):
        rb = self.sender()

        try:
            self.graph.engine.set_cutoff(float(rb.text() or 1000))
        except ValueError as e:
            logging.warning(e)

        self.graph.engine.compute()
        self.graph.update_graph()