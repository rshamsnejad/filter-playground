from PyQt6.QtWidgets import (
    QTabWidget,
    QWidget
)
from lib.Graph.PolezeroGraphWidget import PolezeroGraphWidget
from lib.Graph.BodeGraphWidget import BodeGraphWidget

class ThreeTabWidget(QTabWidget):
    """
    Qt widget containing an input cell's toolbar and graph
    """

    def __init__(self,
        first_tab_widget: QWidget,
        first_tab_label: str,
        bode_graph_widget: BodeGraphWidget,
        *args, **kwargs
    ) -> None:
        """
        Args:
            id (int): The number of the filter to display
        """

        super().__init__(*args, **kwargs)

        self.first_tab_widget = first_tab_widget
        self.bode_graph = bode_graph_widget
        self.polezero_graph = PolezeroGraphWidget()

        self.addTab(self.first_tab_widget, first_tab_label)
        self.addTab(self.bode_graph, "Bode plot")
        self.addTab(self.polezero_graph, "Pole-zero map")

    def compute_and_update(self) -> None:

        self.engine.compute()
        self.bode_graph.update_graph()
        self.polezero_graph.update_graph()
