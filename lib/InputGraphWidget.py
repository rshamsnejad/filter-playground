from lib.GraphWidget import GraphWidget

class InputGraphWidget(GraphWidget):
    """
    Qt widget to display a input cell's graph
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.compute_and_update()

    def update_axvlines(self) -> None:
        """
        Updates the dotted vertical lines depending on
        the computed filter.
        """

        self.axline_mag[0].set_xdata([self.engine.get_frequency()])
        self.axline_phase[0].set_xdata([self.engine.get_frequency()])
