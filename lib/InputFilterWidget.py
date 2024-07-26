import logging
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout
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
        self.filter_toolbar.filter_parameters.field_order.valueChanged.connect(self.handle_order)
        self.filter_toolbar.filter_parameters.field_frequency.valueChanged.connect(self.handle_frequency)
        self.filter_toolbar.filter_parameters.field_gain.valueChanged.connect(self.handle_gain)
        self.filter_toolbar.filter_parameters.field_Q.valueChanged.connect(self.handle_Q)

        self.layout().addWidget(self.filter_toolbar)
        self.layout().addWidget(self.graph)

        self.disable_unused_fields()

    def handle_type(self, filter_type: str):
        try:
            self.graph.engine.set_filtertype(filter_type or 'highpass')
        except ValueError as e:
            logging.warning(e)

        self.disable_unused_fields()

        self.graph.compute_and_update()

    def handle_order(self, order: int):
        try:
            self.graph.engine.set_order(order or 1)
        except ValueError as e:
            logging.warning(e)

        self.graph.compute_and_update()

    def handle_frequency(self, frequency: float):
        try:
            self.graph.engine.set_frequency(frequency or 1000)
        except ValueError as e:
            logging.warning(e)

        self.graph.compute_and_update()

    def handle_gain(self, gain: float):
        try:
            self.graph.engine.set_gain(gain or 0)
        except ValueError as e:
            logging.warning(e)

        self.graph.compute_and_update()

    def handle_Q(self, Q: float):
        try:
            self.graph.engine.set_Q(Q or 0.71)
        except ValueError as e:
            logging.warning(e)

        self.graph.compute_and_update()

    def disable_unused_fields(self) -> None:
        match self.graph.engine.get_filtertype().lower():
            case "highpass" | "lowpass":
                self.filter_toolbar.filter_parameters.field_order.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_frequency.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_gain.setValue(0)
                self.filter_toolbar.filter_parameters.field_gain.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_Q.setValue(0.71)
                self.filter_toolbar.filter_parameters.field_Q.setDisabled(True)

            case "allpass":
                self.filter_toolbar.filter_parameters.field_order.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_frequency.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_gain.setValue(0)
                self.filter_toolbar.filter_parameters.field_gain.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_Q.setDisabled(False)

            case "peak" | "highshelf" | "lowshelf":
                self.filter_toolbar.filter_parameters.field_order.setValue(2)
                self.filter_toolbar.filter_parameters.field_order.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_frequency.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_gain.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_Q.setDisabled(False)

            case _:
                raise ValueError("Unknown filter type")
