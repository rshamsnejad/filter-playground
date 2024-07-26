from lib.GraphWidget import GraphWidget

class OutputGraphWidget(GraphWidget):
    """
    Qt widget to display the output graph
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for i in range(len(self.engine.input_engines) - 1):
            self.add_axvline()

        self.engine.compute()
        self.update_graph()

    def update_axvlines(self) -> None:
        """
        Updates the dotted vertical lines depending on
        the computed filter.
        """

        i = 0
        for engine in self.engine.input_engines:
            self.axline_mag[i].set_xdata([engine.get_frequency()])
            self.axline_phase[i].set_xdata([engine.get_frequency()])
            i += 1

    def add_axvline(self) -> None:
        """
        Adds a new dotted vertical line
        """

        self.axline_mag.append(self.axs[0].axvline(0, linestyle='--', color='red'))
        self.axline_phase.append(self.axs[1].axvline(0, linestyle='--', color='red'))

    def remove_last_axvline(self) -> None:
        """
        Removes the last dotted vertical line
        """

        self.axline_mag[-1].remove()
        del self.axline_mag[-1]
        self.axline_phase[-1].remove()
        del self.axline_phase[-1]
