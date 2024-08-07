from lib.Output.OutputBodeGraphWidget import OutputBodeGraphWidget
from lib.Engine.SumEngine import SumEngine

class SumOutputBodeGraphWidget(OutputBodeGraphWidget):
    """
    Qt widget to display the output graph
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    def set_engine(self, engine: SumEngine) -> None:
        """
        Set the computing engine. Has to be done outside of constructor
        otherwise the input widget and the output widget are inter-dependent

        Args:
            engine (GraphEngine): The engine to use to compute the graph
        """

        self.engine = engine

        for cascade_engine in self.engine.input_engines:
            for engine in cascade_engine.input_engines:
                self.add_axvline()
        
        self.compute_and_update()

    def update_axvlines(self) -> None:
        """
        Updates the dotted vertical lines depending on
        the computed filter.
        """

        i = 0
        for cascade_engine in self.engine.input_engines:
            for engine in cascade_engine.input_engines:
                self.axline_mag[i].set_xdata([engine.get_frequency()])
                self.axline_phase[i].set_xdata([engine.get_frequency()])
                i += 1
