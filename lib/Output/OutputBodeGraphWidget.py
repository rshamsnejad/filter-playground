from lib.Graph.BodeGraphWidget import BodeGraphWidget
from lib.Engine.CascadeEngine import CascadeEngine

class OutputBodeGraphWidget(BodeGraphWidget):
    """
    Qt widget to display the output graph
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    def set_engine_specific(self, engine: CascadeEngine) -> None:
        """
        Set the computing engine. Has to be done outside of constructor
        otherwise the input widget and the output widget are inter-dependent

        Args:
            engine (CascadeEngine): The engine to use to compute the graph
        """

        self.engine = engine

        for i in range(len(self.engine.input_engines) - 1):
            self.add_axvline()

    def update_axvlines(self) -> None:
        """
        Updates the dotted vertical lines depending on
        the computed filter.
        """

        i = 0
        for engine in self.engine.input_engines:
            self.axline_top[i].set_xdata([engine.get_frequency()])
            self.axline_bottom[i].set_xdata([engine.get_frequency()])
            i += 1

    def add_axvline(self, frequency: float = 0) -> None:
        """
        Adds a new dotted vertical line
        """

        self.axline_top.append(self.axs[0].axvline(frequency, linestyle='--', color='red'))
        self.axline_bottom.append(self.axs[1].axvline(frequency, linestyle='--', color='red'))

    def remove_last_axvline(self) -> None:
        """
        Removes the last dotted vertical line
        """

        self.axline_top[-1].remove()
        del self.axline_top[-1]
        self.axline_bottom[-1].remove()
        del self.axline_bottom[-1]
