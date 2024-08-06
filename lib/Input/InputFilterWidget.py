import logging
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout
)
from lib.Input.FilterToolbarWidget import FilterToolbarWidget
from lib.Graph.DualGraphWidget import DualGraphWidget
from lib.Input.InputBodeGraphWidget import InputBodeGraphWidget
from lib.Engine.BiquadEngine import BiquadEngine

class InputFilterWidget(QWidget):
    """
    Qt widget containing an input cell's toolbar and graph
    """

    def __init__(self, id: int, *args, **kwargs) -> None:
        """
        Args:
            id (int): The number of the filter to display
        """

        super().__init__(*args, **kwargs)

        self.id = id

        self.setLayout(QVBoxLayout())

        self.filter_toolbar = FilterToolbarWidget(self.id)
        self.filter_toolbar.setFixedHeight(165)

        self.bode_graph = InputBodeGraphWidget()
        self.dualgraph = DualGraphWidget(self.bode_graph)
        self.dualgraph.set_engine(BiquadEngine())

        self.filter_toolbar.filter_type.combo_box.currentTextChanged.connect(self.handle_type)
        self.filter_toolbar.filter_parameters.field_order.valueChanged.connect(self.handle_order)
        self.filter_toolbar.filter_parameters.field_frequency.valueChanged.connect(self.handle_frequency)
        self.filter_toolbar.filter_parameters.field_gain.valueChanged.connect(self.handle_gain)
        self.filter_toolbar.filter_parameters.field_Q.valueChanged.connect(self.handle_Q)

        self.layout().addWidget(self.filter_toolbar)
        self.layout().addWidget(self.dualgraph)

        self.disable_unused_fields()

    def handle_type(self, filter_type: str) -> None:
        """
        Qt slot to update the filter type according to
        the drop-down list in the toolbar
        """

        try:
            self.dualgraph.engine.set_filtertype(filter_type or 'highpass')
        except ValueError as e:
            logging.warning(e)

        self.disable_unused_fields()

        self.dualgraph.compute_and_update()

    def handle_order(self, order: int) -> None:
        """
        Qt slot to update the filter order according to
        the spinbox in the toolbar
        """

        try:
            self.dualgraph.engine.set_order(order or 1)
        except ValueError as e:
            logging.warning(e)

        self.dualgraph.compute_and_update()

    def handle_frequency(self, frequency: int) -> None:
        """
        Qt slot to update the filter frequency according to
        the spinbox in the toolbar
        """

        try:
            self.dualgraph.engine.set_frequency(frequency or 1000)
        except ValueError as e:
            logging.warning(e)

        self.dualgraph.compute_and_update()

    def handle_gain(self, gain: float) -> None:
        """
        Qt slot to update the filter gain according to
        the spinbox in the toolbar
        """

        try:
            self.dualgraph.engine.set_gain(gain or 0)
        except ValueError as e:
            logging.warning(e)

        self.dualgraph.compute_and_update()

    def handle_Q(self, Q: float) -> None:
        """
        Qt slot to update the filter Q according to
        the spinbox in the toolbar
        """

        try:
            self.dualgraph.engine.set_Q(Q or 0.71)
        except ValueError as e:
            logging.warning(e)

        self.dualgraph.compute_and_update()

    def disable_unused_fields(self) -> None:
        """
        Disables the spinboxes that are not needed depending
        on the filter type, and sets suitable default values
        """

        match self.dualgraph.engine.get_filtertype().lower():
            case "highpass" | "lowpass":
                self.filter_toolbar.filter_parameters.field_order.setValue(2)
                self.filter_toolbar.filter_parameters.field_order.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_frequency.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_gain.setValue(0)
                self.filter_toolbar.filter_parameters.field_gain.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_Q.setDisabled(False)

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

            case "bessel highpass" | "bessel lowpass" \
                | "butterworth highpass" | "butterworth lowpass" \
                | "chebyshev i highpass" | "chebyshev i lowpass" \
                | "chebyshev ii highpass" | "chebyshev ii lowpass" \
                | "elliptic highpass" | "elliptic lowpass":
                self.filter_toolbar.filter_parameters.field_order.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_frequency.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_gain.setValue(0)
                self.filter_toolbar.filter_parameters.field_gain.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_Q.setValue(0.71)
                self.filter_toolbar.filter_parameters.field_Q.setDisabled(True)

            case _:
                raise ValueError("Unknown filter type")
