from PyQt6.QtWidgets import (
    QTabWidget
)

from lib.BodeGraphWidget import BodeGraphWidget
from lib.GraphEngine import GraphEngine

class DualGraphWidget(QTabWidget):

    def __init__(self,
        bode_graph: BodeGraphWidget,
        *args, **kwargs
    ) -> None:

        super().__init__(*args, **kwargs)

        self.bode_graph = bode_graph

        self.addTab(self.bode_graph, "Bode plot")

    def set_engine(self, engine: GraphEngine) -> None:

        self.engine = engine

        self.bode_graph.set_engine(self.engine)

    def compute_and_update(self) -> None:

        self.bode_graph.compute_and_update()