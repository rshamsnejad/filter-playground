from lib.GraphWidget import GraphWidget

class InputGraphWidget(GraphWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.compute_and_update()

    def update_axvlines(self) -> None:
        self.axline_mag[0].set_xdata([self.engine.get_frequency()])
        self.axline_phase[0].set_xdata([self.engine.get_frequency()])

