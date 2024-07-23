from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout
)
from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter

from lib.ButterEngine import ButterEngine

class GraphWidget(QWidget):
    '''
    QT widget for displaying a matplotlib graph with toolbar
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setLayout(QVBoxLayout())

        self.canvas = FigureCanvas(Figure())
        self.figure = self.canvas.figure
        self.axs = self.figure.subplots(2, 1, sharex=True)

        self.layout().addWidget(NavigationToolbar(self.canvas))
        self.layout().addWidget(self.canvas)

        self.filter_engine = ButterEngine()

        self.init_graph()
        self.filter_engine.compute_filter()
        self.update_graph()

    def init_graph(self,
            freq_range:     list[float] = [20, 20e3],
            mag_range:      list[float] = [-40, 10],
            phase_range:    list[float] = [-200, 200]
    ) -> None:
        '''
        Prepares an empty graph to host filter data later on.
        '''

        # Magnitude
        self.magnitude_graph, = self.axs[0].semilogx([], [])
        self.axs[0].set_xlim(freq_range)
        self.axs[0].set_ylabel('Gain [dB]')
        self.axs[0].set_ylim(mag_range)
        self.axs[0].margins(0, 0.1)
        self.axs[0].grid(which='both', axis='both')
        self.axline_mag = self.axs[0].axvline(0, linestyle='--', color='red')

        # Phase
        self.phase_graph, = self.axs[1].semilogx([], [])
        self.axs[1].set_xlabel('Frequency [Hz]')
        self.axs[1].set_xlim(freq_range)
        self.axs[1].set_ylabel('Phase [°]')
        self.axs[1].set_ylim(phase_range)
        self.axs[1].margins(0, 0.1)
        self.axs[1].grid(which='both', axis='both')
        self.axline_phase = self.axs[1].axvline(0, linestyle='--', color='red')

        self.axs[1].xaxis.set_major_formatter(ScalarFormatter())
        self.axs[1].ticklabel_format(axis='x', style='plain')

    def update_graph(self) -> None:
        self.update_title()

        self.magnitude_graph.set_data(
            self.filter_engine.get_frequencies(),
            self.filter_engine.get_magnitude()
        )
        self.phase_graph.set_data(
            self.filter_engine.get_frequencies(),
            self.filter_engine.get_phase()
        )

        self.axline_mag.set_xdata([self.filter_engine.get_cutoff()])
        self.axline_phase.set_xdata([self.filter_engine.get_cutoff()])

        self.magnitude_graph.figure.canvas.draw()
        self.phase_graph.figure.canvas.draw()

    def update_title(self) -> None:
        self.figure.suptitle(
            (
                f"Butterworth {self.filter_engine.get_filtertype().lower()} filter, "
                f"order {self.filter_engine.get_order()}, "
                f"$f_0 = {self.filter_engine.get_cutoff()}$ Hz"
            )
        )


