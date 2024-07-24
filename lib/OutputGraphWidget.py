from lib.GraphWidget import GraphWidget

class OutputGraphWidget(GraphWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for engine in self.engine.input_engines:
            self.axline_mag.append(self.axs[0].axvline(0, linestyle='--', color='red'))
            self.axline_phase.append(self.axs[1].axvline(0, linestyle='--', color='red'))

        self.engine.compute()
        self.update_graph()

    def update_axvlines(self) -> None:

        i = 0
        for engine in self.engine.input_engines:
            self.axline_mag[i].set_xdata([engine.get_cutoff()])
            self.axline_phase[i].set_xdata([engine.get_cutoff()])
            i += 1

