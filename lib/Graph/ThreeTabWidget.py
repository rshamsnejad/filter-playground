import logging

from PyQt6.QtWidgets import (
    QTabWidget,
    QWidget,
    QMessageBox
)
from lib.Engine.GraphEngine import GraphEngine
from lib.Graph.PolezeroGraphWidget import PolezeroGraphWidget
from lib.Graph.BodeGraphWidget import BodeGraphWidget

class ThreeTabWidget(QTabWidget):
    """
    Base class for displaying 3 tabs for parameters,
    Bode plot and pole-zero map.
    """

    def __init__(self,
        first_tab_widget: QWidget,
        first_tab_label: str,
        bode_graph_widget: BodeGraphWidget,
        *args, **kwargs
    ) -> None:
        """
        Args:
            first_tab_widget (QWidget): The Qt widget to diplay in the first tab
            first_tab_label (str): Label of the first tab
            bode_graph_widget (BodeGraphWidget): The Bode graph widget to display in the second tab
        """

        super().__init__(*args, **kwargs)

        self.first_tab_widget = first_tab_widget
        self.bode_graph = bode_graph_widget
        self.polezero_graph = PolezeroGraphWidget()

        self.addTab(self.first_tab_widget, first_tab_label)
        self.addTab(self.bode_graph, "Bode plot")
        self.addTab(self.polezero_graph, "Pole-zero map")

        self.popup = QMessageBox()

    def set_engine(self, engine: GraphEngine) -> None:
        """
        Set the computing engine. Has to be done outside of constructor
        otherwise the input widget and the output widget are inter-dependent.

        Args:
            engine (GraphEngine): The engine to use to compute the graph
        """

        self.engine = engine

        self.bode_graph.set_engine(self.engine)
        self.polezero_graph.set_engine(self.engine)

    def popup_invalid_data(self, message: str) -> None:
        """
        Displays a popup for ValueError exceptions

        Args:
            message (str): The message to display inside the popup window
        """

        self.popup.setWindowTitle("Invalid data")
        self.popup.setIcon(QMessageBox.Icon.Warning)
        self.popup.setText(message)

        self.popup.exec()

    def compute_and_update(self) -> None:
        """
        Convenience method to wrap computing the filter
        and updating the two graphs in one go
        """

        self.engine.compute()

        self.bode_graph.update_graph()
        self.polezero_graph.update_graph()

    def handle_sample_frequency(self, sample_frequency: str) -> None:
        """
        Qt slot to update the sample frequency according to
        the drop-down list in the main window toolbar
        """

        self.engine.set_sample_frequency(float(sample_frequency or 48000))

        self.compute_and_update()

    def handle_flip_phase(self, flip_phase: bool) -> None:
        """
        Qt slot to update the filter phase flip according
        to the checkbox in the toolbar
        """

        self.engine.set_flip_phase(flip_phase)

    def handle_gain(self, gain: float) -> None:
        """
        Qt slot to update the filter gain according to
        the spinbox in the toolbar
        """

        try:
            self.engine.set_gain(gain or 0)
        except ValueError as e:
            logging.warning(e)
            self.popup_invalid_data(str(e))

    def handle_delay_samples(self, delay_samples: int) -> None:
        """
        Qt slot to update the filter delay according
        to the spinbox in the toolbar
        """

        try:
            self.engine.set_delay(delay_samples or 0)
        except ValueError as e:
            logging.warning(e)
            self.popup_invalid_data(str(e))

        delay_msec = self.engine.convert_samples_to_msec(delay_samples)

        self.update_delay_msec_spinbox(delay_msec)

    def update_delay_msec_spinbox(self, delay_samples: int) -> None:

        raise NotImplementedError

    def update_delay_samples_spinbox(self, delay_samples: int) -> None:

        raise NotImplementedError

    def handle_delay_msec(self, delay_msec: float) -> None:
        """
        Qt slot to update the filter delay in samples
        according to the spinbox in milliseconds in the toolbar
        """

        delay_samples = self.engine.convert_msec_to_samples(delay_msec or 0)

        self.update_delay_samples_spinbox(delay_samples)
