from PyQt6.QtWidgets import (
    QTabWidget,
    QWidget
)
from lib.Input.InputBodeGraphWidget import InputBodeGraphWidget
from lib.Graph.PolezeroGraphWidget import PolezeroGraphWidget
from lib.Engine.GraphEngine import GraphEngine

class ThreeTabWidget(QTabWidget):
    """
    Qt widget containing an input cell's toolbar and graph
    """

    def __init__(self,
        first_tab_widget: QWidget,
        first_tab_label: str,
        engine: GraphEngine,
        *args, **kwargs
    ) -> None:
        """
        Args:
            id (int): The number of the filter to display
        """

        super().__init__(*args, **kwargs)

        self.engine = engine

        self.first_tab_widget = first_tab_widget
        self.bode_graph = InputBodeGraphWidget()
        self.bode_graph.set_engine(self.engine)
        self.polezero_graph = PolezeroGraphWidget()
        self.polezero_graph.set_engine(self.engine)

        self.addTab(self.first_tab_widget, first_tab_label)
        self.addTab(self.bode_graph, "Bode plot")
        self.addTab(self.polezero_graph, "Pole-zero map")

    def compute_and_update(self) -> None:

        self.engine.compute()
        self.bode_graph.update_graph()
        self.polezero_graph.update_graph()
