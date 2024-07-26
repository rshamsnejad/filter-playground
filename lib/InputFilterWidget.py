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
        self.filter_toolbar.filter_parameters.field_order.textChanged.connect(self.handle_order)
        self.filter_toolbar.filter_parameters.field_frequency.textChanged.connect(self.handle_frequency)
        self.filter_toolbar.filter_parameters.field_gain.textChanged.connect(self.handle_gain)
        self.filter_toolbar.filter_parameters.field_Q.textChanged.connect(self.handle_Q)

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

    def handle_order(self, order: str):
        try:
            self.graph.engine.set_order(int(order or 1))
        except ValueError as e:
            logging.warning(e)

        self.graph.compute_and_update()

    def handle_frequency(self, frequency: str):
        try:
            self.graph.engine.set_frequency(float(frequency or 1000))
        except ValueError as e:
            logging.warning(e)

        self.graph.compute_and_update()

    def handle_gain(self, gain: str):
        try:
            self.graph.engine.set_gain(float(gain or 3))
        except ValueError as e:
            logging.warning(e)

        self.graph.compute_and_update()

    def handle_Q(self, Q: str):
        try:
            self.graph.engine.set_Q(float(Q or 0.71))
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

            case "peak":
                self.filter_toolbar.filter_parameters.field_order.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_frequency.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_gain.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_Q.setDisabled(False)

            case _:
                raise ValueError("Unknown filter type")
