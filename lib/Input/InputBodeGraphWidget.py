from lib.Graph.BodeGraphWidget import BodeGraphWidget
from lib.Engine.BiquadEngine import BiquadEngine

class InputBodeGraphWidget(BodeGraphWidget):
    """
    Qt widget to display a input cell's graph
    """

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self.engine = None

    def set_engine(self, engine: BiquadEngine) -> None:
        """
        Set the computing engine. Has to be done outside of constructor
        otherwise the input widget and the output widget are inter-dependent

        Args:
            engine (GraphEngine): The engine to use to compute the graph
        """

        self.engine = engine

        self.compute_and_update()

    def update_axvlines(self) -> None:
        """
        Updates the dotted vertical lines depending on
        the computed filter.
        """

        self.axline_mag[0].set_xdata([self.engine.get_frequency()])
        self.axline_phase[0].set_xdata([self.engine.get_frequency()])
