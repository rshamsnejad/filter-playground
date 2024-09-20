from lib.Output.OutputBodeGraphWidget import OutputBodeGraphWidget
from lib.Engine.SumEngine import SumEngine

class SumOutputBodeGraphWidget(OutputBodeGraphWidget):
    """
    Qt widget to display the output graph
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    def set_engine_specific(self, engine: SumEngine) -> None:
        """
        Set the computing engine. Has to be done outside of constructor
        otherwise the input widget and the output widget are inter-dependent

        Args:
            engine (SumEngine): The engine to use to compute the graph
        """

        self.engine = engine

        for cascade_engine in self.engine.input_engines:
            for engine in cascade_engine.input_engines:
                self.add_axvline()

    def update_axvlines(self) -> None:
        """
        Updates the dotted vertical lines depending on
        the computed filter.
        """

        for axline in self.axline_top:
            axline.remove()
        del self.axline_top
        self.axline_top = []

        for axline in self.axline_bottom:
            axline.remove()
        del self.axline_bottom
        self.axline_bottom = []

        for cascade_engine in self.engine.input_engines:
            for engine in cascade_engine.input_engines:
                self.add_axvline(engine.get_frequency())
