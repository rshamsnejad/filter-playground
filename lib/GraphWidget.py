from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout
)
from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter

from lib.GraphEngine import GraphEngine

class GraphWidget(QWidget):
    """
    Base class for displaying a matplotlib graph with toolbar.

    Must be inherited by a child class implementing the
    virtual method(s)
    """

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self.setLayout(QVBoxLayout())

        self.canvas = FigureCanvas(Figure())
        self.figure = self.canvas.figure
        self.axs = self.figure.subplots(2, 1, sharex=True)

        self.layout().addWidget(NavigationToolbar(self.canvas))
        self.layout().addWidget(self.canvas)

        self.init_graph()

    def set_engine(self, engine: GraphEngine) -> None:
        """
        Set the computing engine. Has to be done outside of constructor
        otherwise the input widget and the output widget are inter-dependent

        Args:
            engine (GraphEngine): The engine to use to compute the graph
        """

        raise NotImplementedError

    def init_graph(self,
            freq_range:     list[float] = [20, 20e3],
            mag_range:      list[float] = [-30, 30],
            phase_range:    list[float] = [-200, 200]
    ) -> None:
        """
        Prepares an empty graph to host filter data later on.

        Args:
            freq_range (list[float], optional):
                Range to display on X axis in Hz. Defaults to [20, 20e3].
            mag_range (list[float], optional):
                Range to display on Y axis of the magnitude plot in dB. Defaults to [-30, 30].
            phase_range (list[float], optional):
                Range to display on the Y axis of the phase plot in degrees. Defaults to [-200, 200].
        """

        self.figure.subplots_adjust(
            left=0.2,
            bottom=0.15,
            right=None,
            top=None,
            wspace=None,
            hspace=None
        )

        # Magnitude
        self.magnitude_graph, = self.axs[0].semilogx([], [])
        self.axs[0].set_xlim(freq_range)
        self.axs[0].set_ylabel('Gain [dB]')
        self.axs[0].set_ylim(mag_range)
        self.axs[0].margins(0, 0.1)
        self.axs[0].grid(which='both', axis='both')

        self.axline_mag = [
            self.axs[0].axvline(0, linestyle='--', color='red')
        ]

        # Phase
        self.phase_graph, = self.axs[1].semilogx([], [])
        self.axs[1].set_xlabel('Frequency [Hz]')
        self.axs[1].set_xlim(freq_range)
        self.axs[1].set_ylabel('Phase [°]')
        self.axs[1].set_ylim(phase_range)
        self.axs[1].margins(0, 0.1)
        self.axs[1].grid(which='both', axis='both')

        self.axline_phase = [
            self.axs[1].axvline(0, linestyle='--', color='red')
        ]

        # Disable scientific notation on the frequency axis
        self.axs[1].xaxis.set_major_formatter(ScalarFormatter())
        self.axs[1].ticklabel_format(axis='x', style='plain')

    def update_graph(self) -> None:
        """
        Updates the graph with the data currently stored in the object.
        Usually called after self.engine.compute()
        """

        self.update_title()

        self.magnitude_graph.set_data(
            self.engine.get_frequencies(),
            self.engine.get_magnitude()
        )
        self.phase_graph.set_data(
            self.engine.get_frequencies(),
            self.engine.get_phase()
        )

        self.update_axvlines()

        self.magnitude_graph.figure.canvas.draw()
        self.phase_graph.figure.canvas.draw()

    def update_title(self) -> None:
        """
        Updates the graph title depending on the filter type
        """

        self.figure.suptitle(self.engine.generate_title())

    def compute_and_update(self) -> None:
        """
        Convenience method to wrap computing the filter
        and updating the graph in one go
        """

        self.engine.compute()
        self.update_graph()

    def update_axvlines(self) -> None:
        """
        Updates the dotted vertical lines depending on
        the computed filter.

        To be implemented by child classes.
        """

        raise NotImplementedError