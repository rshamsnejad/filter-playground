from lib.GraphWidget import GraphWidget

class InputGraphWidget(GraphWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.engine.compute()
        self.update_graph()

    def update_axvlines(self) -> None:
        self.axline_mag[0].set_xdata([self.engine.get_frequency()])
        self.axline_phase[0].set_xdata([self.engine.get_frequency()])

