import logging

from lib.Graph.ThreeTabWidget import ThreeTabWidget
from lib.Engine.BiquadEngine import BiquadEngine

from PyQt6.QtWidgets import QSizePolicy

class InputFilterWidget(ThreeTabWidget):
    """
    Qt widget containing an input cell's toolbar and graph
    """

    def __init__(self,
        id: int,
        engine: BiquadEngine,
        *args, **kwargs
    ) -> None:
        """
        Args:
            id (int): The number of the filter to display
            engine (BiquadEngine): The engine to use for computation
        """

        super().__init__(*args, **kwargs)

        self.id = id
        self.engine = engine

        self.filter_toolbar = self.first_tab_widget
        policy = QSizePolicy()
        policy.setVerticalPolicy(QSizePolicy.Policy.Minimum)
        self.filter_toolbar.setSizePolicy(policy)

        self.bode_graph.set_engine(self.engine)
        self.polezero_graph.set_engine(self.engine)

        self.filter_toolbar.filter_type.combo_box.currentTextChanged.connect(self.handle_type)
        self.filter_toolbar.filter_parameters.field_order.valueChanged.connect(self.handle_order)
        self.filter_toolbar.filter_parameters.field_frequency.valueChanged.connect(self.handle_frequency)
        self.filter_toolbar.filter_parameters.field_gain.valueChanged.connect(self.handle_gain)
        self.filter_toolbar.filter_parameters.field_Q.valueChanged.connect(self.handle_Q)
        self.filter_toolbar.filter_parameters.field_flip_phase.stateChanged.connect(self.handle_flip_phase)
        self.filter_toolbar.filter_parameters.field_passband_ripple.valueChanged.connect(self.handle_passband_ripple)
        self.filter_toolbar.filter_parameters.field_stopband_attenuation.valueChanged.connect(self.handle_stopband_attenuation)
        self.filter_toolbar.filter_parameters.field_transband_width.valueChanged.connect(self.handle_transband_width)

        self.disable_unused_fields()

    def handle_type(self, filter_type: str) -> None:
        """
        Qt slot to update the filter type according to
        the drop-down list in the toolbar
        """

        try:
            self.engine.set_filtertype(filter_type or 'highpass')
        except ValueError as e:
            logging.warning(e)

        self.disable_unused_fields()

        self.compute_and_update()

    def handle_order(self, order: int) -> None:
        """
        Qt slot to update the filter order according to
        the spinbox in the toolbar
        """

        try:
            self.engine.set_order(order or 1)
        except ValueError as e:
            logging.warning(e)

        self.compute_and_update()

    def handle_frequency(self, frequency: int) -> None:
        """
        Qt slot to update the filter frequency according to
        the spinbox in the toolbar
        """

        try:
            self.engine.set_frequency(frequency or 1000)
        except ValueError as e:
            logging.warning(e)

        self.compute_and_update()

    def handle_Q(self, Q: float) -> None:
        """
        Qt slot to update the filter Q according to
        the spinbox in the toolbar
        """

        try:
            self.engine.set_Q(Q or 0.71)
        except ValueError as e:
            logging.warning(e)

        self.compute_and_update()

    def handle_passband_ripple(self, passband_ripple: float) -> None:
        """
        Qt slot to update the maximum passband ripple
        according to the spinbox in the toolbar
        """

        try:
            self.engine.set_passband_ripple(passband_ripple or 3)
        except ValueError as e:
            logging.warning(e)

        self.compute_and_update()

    def handle_stopband_attenuation(self, stopband_attenuation: float) -> None:
        """
        Qt slot to update the minimum stopband attenuation
        according to the spinbox in the toolbar
        """

        try:
            self.engine.set_stopband_attenuation(stopband_attenuation or 60)
        except ValueError as e:
            logging.warning(e)

        self.compute_and_update()

    def handle_transband_width(self, transband_width: int) -> None:
        """
        Qt slot to update the transition band width
        according to the spinbox in the toolbar
        """

        try:
            self.engine.set_transband_width(transband_width or 300)
        except ValueError as e:
            logging.warning(e)

        self.compute_and_update()

    def disable_unused_fields(self) -> None:
        """
        Disables the spinboxes that are not needed depending
        on the filter type, and sets suitable default values
        """

        match self.engine.get_filtertype().lower():
            case "highpass" | "lowpass":
                self.filter_toolbar.filter_parameters.field_order.setValue(2)
                self.filter_toolbar.filter_parameters.field_order.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_frequency.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_gain.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_Q.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_passband_ripple.setValue(3)
                self.filter_toolbar.filter_parameters.field_passband_ripple.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_stopband_attenuation.setValue(60)
                self.filter_toolbar.filter_parameters.field_stopband_attenuation.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_transband_width.setDisabled(True)

            case "allpass":
                self.filter_toolbar.filter_parameters.field_order.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_frequency.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_gain.setValue(0)
                self.filter_toolbar.filter_parameters.field_gain.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_Q.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_passband_ripple.setValue(3)
                self.filter_toolbar.filter_parameters.field_passband_ripple.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_stopband_attenuation.setValue(60)
                self.filter_toolbar.filter_parameters.field_stopband_attenuation.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_transband_width.setDisabled(True)

            case "peak" | "highshelf" | "lowshelf":
                self.filter_toolbar.filter_parameters.field_order.setValue(2)
                self.filter_toolbar.filter_parameters.field_order.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_frequency.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_gain.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_Q.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_passband_ripple.setValue(3)
                self.filter_toolbar.filter_parameters.field_passband_ripple.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_stopband_attenuation.setValue(60)
                self.filter_toolbar.filter_parameters.field_stopband_attenuation.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_transband_width.setDisabled(True)

            case "bessel highpass" | "bessel lowpass" \
                | "butterworth highpass" | "butterworth lowpass":
                self.filter_toolbar.filter_parameters.field_order.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_frequency.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_gain.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_Q.setValue(0.71)
                self.filter_toolbar.filter_parameters.field_Q.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_passband_ripple.setValue(3)
                self.filter_toolbar.filter_parameters.field_passband_ripple.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_stopband_attenuation.setValue(60)
                self.filter_toolbar.filter_parameters.field_stopband_attenuation.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_transband_width.setDisabled(True)

            case "chebyshev i highpass" | "chebyshev i lowpass":
                self.filter_toolbar.filter_parameters.field_order.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_frequency.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_gain.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_Q.setValue(0.71)
                self.filter_toolbar.filter_parameters.field_Q.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_passband_ripple.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_stopband_attenuation.setValue(60)
                self.filter_toolbar.filter_parameters.field_stopband_attenuation.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_transband_width.setDisabled(True)

            case "chebyshev ii highpass" | "chebyshev ii lowpass":
                self.filter_toolbar.filter_parameters.field_order.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_frequency.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_gain.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_Q.setValue(0.71)
                self.filter_toolbar.filter_parameters.field_Q.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_passband_ripple.setValue(3)
                self.filter_toolbar.filter_parameters.field_passband_ripple.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_stopband_attenuation.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_transband_width.setDisabled(True)

            case "elliptic highpass" | "elliptic lowpass":
                self.filter_toolbar.filter_parameters.field_order.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_frequency.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_gain.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_Q.setValue(0.71)
                self.filter_toolbar.filter_parameters.field_Q.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_passband_ripple.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_stopband_attenuation.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_transband_width.setDisabled(True)

            case "fir highpass" | "fir lowpass":
                self.filter_toolbar.filter_parameters.field_order.setValue(2)
                self.filter_toolbar.filter_parameters.field_order.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_frequency.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_gain.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_Q.setValue(0.71)
                self.filter_toolbar.filter_parameters.field_Q.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_passband_ripple.setValue(3)
                self.filter_toolbar.filter_parameters.field_passband_ripple.setDisabled(True)
                self.filter_toolbar.filter_parameters.field_stopband_attenuation.setDisabled(False)
                self.filter_toolbar.filter_parameters.field_transband_width.setDisabled(False)

            case _:
                raise ValueError("Unknown filter type")
