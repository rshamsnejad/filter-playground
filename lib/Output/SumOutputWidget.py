from lib.Engine.SumEngine import SumEngine
from lib.Graph.ThreeTabWidget import ThreeTabWidget
from lib.Input.InputFilterWidget import InputFilterWidget

class SumOutputWidget(ThreeTabWidget):
    """
    Qt widget for the output filter sum
    """

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self.sum_toolbar = self.first_tab_widget

        # Show Bode plot on load
        self.setCurrentIndex(1)

    def set_engine(self, engine: SumEngine) -> None:

        self.engine = engine
        self.bode_graph.set_engine(self.engine)
        self.polezero_graph.set_engine(self.engine)
