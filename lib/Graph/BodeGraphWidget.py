from matplotlib.ticker import ScalarFormatter

from lib.Graph.GraphWidget import GraphWidget
from lib.Engine.GraphEngine import GraphEngine

import numpy as np

class BodeGraphWidget(GraphWidget):
    """
    Base class for displaying a matplotlib Bode plot with toolbar.

    Must be inherited by a child class implementing the
    virtual method(s)
    """

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self.axs = self.figure.subplots(2, 1, sharex=True)
        self.axvspans = [None, None]
        self.axvspan_texts = [None, None]

        self.init_graph()

    def set_engine(self, engine: GraphEngine) -> None:
        """
        Set the computing engine. Has to be done outside of constructor
        otherwise the input widget and the output widget are inter-dependent.

        To be implemented by child classes

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

        # Magnitude
        self.magnitude_graph, = self.axs[0].semilogx([], [])
        self.axs[0].set_xlim(freq_range)
        self.axs[0].set_ylabel('Gain [dB]')
        self.axs[0].set_ylim(mag_range)
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
        self.axs[1].grid(which='both', axis='both')

        phase_color = 'C0'
        self.axs[1].tick_params(axis='y', colors=phase_color)
        self.axs[1].yaxis.label.set_color(phase_color)

        # Group delay
        gd_color = 'salmon'
        self.gd_ax = self.axs[1].twinx()
        self.gd_ax.set_ylabel("Group delay [ms]")
        self.gd_ax.set_ylim([0, 10])
        self.gd_graph, = self.gd_ax.semilogx([], [], color=gd_color)
        self.gd_ax.tick_params(axis='y', colors=gd_color)
        self.gd_ax.yaxis.label.set_color(gd_color)

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
            self.engine.get_magnitude_db()
        )
        self.phase_graph.set_data(
            self.engine.get_frequencies(),
            self.engine.get_phase_deg_nan()
        )
        self.gd_graph.set_data(
            self.engine.get_frequencies()[:-1],
            self.engine.get_group_delay_ms()
        )

        # Drop first group delay point for determining the maximum
        # as it is garbage and can be way too high
        gd_max =  np.max(np.ma.masked_invalid(self.engine.get_group_delay_ms()[1:]))
        ylim_max = gd_max + (gd_max / 10)

        self.gd_ax.set_ylim(0, ylim_max)

        self.update_axvlines()

        # Grey out the area above Nyquist frequency
        for axvspan in self.axvspans:
            if axvspan:
                axvspan.remove()
        del self.axvspans
        self.axvspans = []

        for axvspan_text in self.axvspan_texts:
            if axvspan_text:
                axvspan_text.remove()
        del self.axvspan_texts
        self.axvspan_texts = []

        for ax in self.axs:
            self.axvspans.append(ax.axvspan(self.engine.get_sample_frequency() / 2, 1e12, color='gray'))
            self.axvspan_texts.append(
                ax.text(
                    (self.engine.get_sample_frequency() / 2) * 1.1,
                    0,
                    "Harry Nyquist\nis watching you",
                    fontsize=10,
                    fontweight='black',
                    color='ivory',
                    horizontalalignment='left',
                    verticalalignment='center',
                    clip_on=True
                )
            )

        self.canvas.draw()

    def update_axvlines(self) -> None:
        """
        Updates the dotted vertical lines depending on
        the computed filter.

        To be implemented by child classes.
        """

        raise NotImplementedError