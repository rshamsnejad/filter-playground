import logging
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout
)
from lib.FilterToolbarWidget import FilterToolbarWidget
from lib.GraphWidget import GraphWidget
from lib.ButterEngine import ButterEngine

class InputFilterWidget(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setLayout(QVBoxLayout())

        self.graph = GraphWidget(ButterEngine())
        self.filter_toolbar = FilterToolbarWidget()

        for button in self.filter_toolbar.filter_type.radio_buttons:
            button.toggled.connect(self.handle_type)

        self.filter_toolbar.filter_parameters.field_order.textChanged.connect(self.handle_order)
        self.filter_toolbar.filter_parameters.field_cutoff.textChanged.connect(self.handle_cutoff)

        self.layout().addWidget(self.filter_toolbar)
        self.layout().addWidget(self.graph)

    def handle_type(self):
        rb = self.sender()

        try:
            self.graph.engine.set_filtertype(rb.text() or 'highpass')
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
            self.graph.engine.set_cutoff(int(rb.text() or 1000))
        except ValueError as e:
            logging.warning(e)

        self.graph.engine.compute()
        self.graph.update_graph()