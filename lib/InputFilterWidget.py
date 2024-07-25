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

        self.filter_toolbar.filter_type.combo_box.currentTextChanged.connect(self.handle_type)
        self.filter_toolbar.filter_parameters.field_order.textChanged.connect(self.handle_order)
        self.filter_toolbar.filter_parameters.field_frequency.textChanged.connect(self.handle_frequency)

        self.layout().addWidget(self.filter_toolbar)
        self.layout().addWidget(self.graph)

    def handle_type(self, filter_type: str):
        try:
            self.graph.engine.set_filtertype(filter_type or 'highpass')
        except ValueError as e:
            logging.warning(e)

        self.graph.engine.compute()
        self.graph.update_graph()

    def handle_order(self, order: str):
        try:
            self.graph.engine.set_order(int(order or 1))
        except ValueError as e:
            logging.warning(e)

        self.graph.engine.compute()
        self.graph.update_graph()

    def handle_frequency(self, frequency: str):
        try:
            self.graph.engine.set_frequency(float(frequency or 1000))
        except ValueError as e:
            logging.warning(e)

        self.graph.engine.compute()
        self.graph.update_graph()