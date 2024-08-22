import logging

from PyQt6.QtWidgets import (
    QTabWidget,
    QWidget,
    QMessageBox
)
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
        self.compute_and_update()

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

        self.compute_and_update()