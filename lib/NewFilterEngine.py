import numpy as np
from scipy import signal

from PyQt6.QtWidgets import QGridLayout

from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter


class NewFilterEngine:
    def __init__(self,
        order:      int = 4,
        cutoff:     float = 1000,
        filtertype: str = "highpass"
    ) -> None:
        self.set_order(order)
        self.set_cutoff(cutoff)
        self.set_filtertype(filtertype)

        self.__filter = {
            "frequencies": [],
            "magnitude": [],
            "phase": []
        }

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

    def get_frequencies(self) -> list[float]:
        return self.__filter['frequencies']

    def get_magnitude(self) -> list[float]:
        return self.__filter['magnitude']

    def get_phase(self) -> list[float]:
        return self.__filter['phase']

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
