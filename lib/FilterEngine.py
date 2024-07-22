import numpy as np
from scipy import signal

from PyQt6.QtWidgets import QGridLayout

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter


class FilterEngine:
    def __init__(self, layout: QGridLayout) -> None:
        self.set_order(4)
        self.set_cutoff(165)
        self.set_filtertype('highpass')

        self.__canvas = FigureCanvas(Figure())
        self.__fig = self.__canvas.figure
        self.__axs = self.__fig.subplots(2, 1, sharex=True)

        layout.addWidget(self.__canvas, 3, 0, 1, -1)

        plot_freq_range     = [20, 20e3]
        plot_mag_range      = [-40, 10]
        plot_phase_range    = [-200, 200]

        self.update_title()
        self.compute_filter()

        # Magnitude
        self.__mag, = self.__axs[0].semilogx(self.__filter['frequencies'], self.__filter['magnitude'])
        self.__axs[0].set_xlim(plot_freq_range)
        self.__axs[0].set_ylabel('Gain [dB]')
        self.__axs[0].set_ylim(plot_mag_range)
        self.__axs[0].margins(0, 0.1)
        self.__axs[0].grid(which='both', axis='both')
        self.__axline_mag = self.__axs[0].axvline(self.__cutoff, linestyle='--', color='red')

        # Phase
        self.__phase, = self.__axs[1].semilogx(self.__filter['frequencies'], self.__filter['phase'])
        self.__axs[1].set_xlabel('Frequency [Hz]')
        self.__axs[1].set_xlim(plot_freq_range)
        self.__axs[1].set_ylabel('Phase [°]')
        self.__axs[1].set_ylim(plot_phase_range)
        self.__axs[1].margins(0, 0.1)
        self.__axs[1].grid(which='both', axis='both')
        self.__axline_phase = self.__axs[1].axvline(self.__cutoff, linestyle='--', color='red')

        self.__axs[1].xaxis.set_major_formatter(ScalarFormatter())
        self.__axs[1].ticklabel_format(axis='x', style='plain')

    def set_order(self, order: int) -> None:
        if order <= 0:
            self.__order = 1
            raise ValueError("Order must be a positive integer")
        else:
            self.__order = order

    def get_order(self) -> int:
        return self.__order

    def set_cutoff(self, cutoff: float) -> None:
        if cutoff < 1:
            self.__cutoff = 1000
            raise ValueError("Cutoff must be a positive value")
        else:
            self.__cutoff = cutoff

    def get_cutoff(self) -> float:
        return self.__cutoff

    def set_filtertype(self, filtertype: str) -> None:
        if filtertype.casefold() not in ["highpass", "lowpass", "bandpass", "bandstop"]:
            self.__filtertype = "highpass"
            raise ValueError("Incorrect filter type")
        else:
            self.__filtertype = filtertype

    def get_filtertype(self) -> str:
        return self.__filtertype

    def compute_filter(self) -> None:
        b, a = signal.butter(self.__order, self.__cutoff, self.__filtertype, True)
        frequencies, magnitude = signal.freqs(b, a, worN=np.logspace(0, 5, 1000))

        mag_db = 20 * np.log10(abs(magnitude))
        phase_deg = np.angle(magnitude, deg=True)
        phase_deg_nan = self.remove_phase_discontinuities(phase_deg)

        self.__filter = {
            "frequencies": frequencies,
            "magnitude": mag_db,
            "phase": phase_deg_nan
        }

    def update_title(self) -> None:
        self.__fig.suptitle(f"Butterworth {self.__filtertype.lower()} filter, order {self.__order}, $f_0 = {self.__cutoff}$ Hz")

    def update_filter(self) -> None:
        self.compute_filter()

        self.update_title()

        self.__mag.set_data(self.__filter['frequencies'], self.__filter['magnitude'])
        self.__phase.set_data(self.__filter['frequencies'], self.__filter['phase'])

        self.__axline_mag.set_xdata([self.__cutoff])
        self.__axline_phase.set_xdata([self.__cutoff])

        self.__mag.figure.canvas.draw()
        self.__phase.figure.canvas.draw()


    def remove_phase_discontinuities(self, phase: list) -> list:
        """
        In a wrapped phase array, replaces the two points before
        each wrap with NaN. This is useful to prevent matplotlib
        from plotting vertical lines at the wrap locations

        Args:
            phase (list): phase points list

        Returns:
            list: input list with NaN before and after each wrap
        """

        # Get sign of each point
        # Negative  gives -1
        # Positive  gives 1
        # Zero      gives 0
        signs = np.sign(phase)

        # Split the list in adjacent pairs
        pairs = []
        for i in range(len(signs) - 1):
            pairs.append( (signs[i], signs[i + 1]) )

        # A pair of (-1, 1) indicates a wrap: find out the indexes of such pairs
        pairs_indexes = [index for index, element in enumerate(pairs) if element == (-1, 1) or element == (1, -1)]

        # Replace all points before the wraps with NaN
        phase_nan = phase.copy()
        phase_nan[pairs_indexes] = np.nan

        return phase_nan
