from PyQt6.QtWidgets import (
    QTabWidget
)

from lib.Graph.BodeGraphWidget import BodeGraphWidget
from lib.Graph.PolezeroGraphWidget import PolezeroGraphWidget
from lib.Engine.GraphEngine import GraphEngine

class DualGraphWidget(QTabWidget):

    def __init__(self,
        bode_graph: BodeGraphWidget,
        *args, **kwargs
    ) -> None:

        super().__init__(*args, **kwargs)

        self.bode_graph = bode_graph
        self.polezero_graph = PolezeroGraphWidget()

        self.addTab(self.bode_graph, "Bode plot")
        self.addTab(self.polezero_graph, "Pole-zero map")

    def set_engine(self, engine: GraphEngine) -> None:

        self.engine = engine

        self.bode_graph.set_engine(self.engine)
        self.polezero_graph.set_engine(self.engine)

    def compute_and_update(self) -> None:

        self.engine.compute()
        self.bode_graph.update_graph()
        self.polezero_graph.update_graph()