from PyQt6.QtCore import QObject
import numpy as np
from scipy.signal import sos2zpk

class GraphEngine(QObject):
    """
    Base class for computing the data to display in a graph

    Must be inherited by a child class implementing the
    virtual method(s)
    """

    def __init__(self,
        flip_phase: bool = False,
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self.filter = {
            "frequencies": [],
            "magnitude": [],
            "magnitude_lin": [],
            "magnitude_db": [],
            "phase_rad": [],
            "phase_deg": [],
            "phase_deg_nan": [],
            "group_delay_ms": []
        }

        self.fs = 48000
        self.frequency_points = 5000
        self.set_flip_phase(flip_phase)

    def compute_specific(self) -> None:
        """
        Compute the specific filter data based on the parameters.

        Must be implemented by child classes
        """

        raise NotImplementedError

    def compute(self) -> None:
        """
        Computes the generic data after the specific data
        """

        self.compute_specific()

        self.wrap_phase()
        self.remove_phase_discontinuities()

        self.generate_zpk()
        self.compute_group_delay()

    def generate_title(self) -> str:
        """
        Create a string to display as graph title.

        Must be implemented by child classes
        """

        raise NotImplementedError

    def get_frequencies(self) -> list[float]:
        """
        Returns:
            list[float]: The X axis frequency values
        """

        return self.filter['frequencies']

    def get_magnitude(self) -> list[float]:
        """
        Returns:
            list[float]: The Y axis complex magnitude values
        """

        return self.filter['magnitude']

    def get_magnitude_lin(self) -> list[float]:
        """
        Returns:
            list[float]: The Y axis real magnitude values in linear form
        """

        return self.filter['magnitude_lin']


    def get_magnitude_db(self) -> list[float]:
        """
        Returns:
            list[float]: The Y axis real magnitude values in dB
        """

        return self.filter['magnitude_db']

    def get_phase_rad(self) -> list[float]:
        """
        Returns:
            list[float]:
                The Y axis phase values in radians
        """

        return self.filter['phase_rad']

    def get_phase_deg(self) -> list[float]:
        """
        Returns:
            list[float]:
                The Y axis phase values in degrees
        """

        return self.filter['phase_deg']

    def get_phase_deg_nan(self) -> list[float]:
        """
        Returns:
            list[float]:
                The Y axis phase values in degrees without discontinuities
        """

        return self.filter['phase_deg_nan']

    def get_group_delay_ms(self) -> list[float]:
        """
        Returns:
            list[float]: The Y axis group delay values
        """

        return self.filter['group_delay_ms']

    def remove_phase_discontinuities(self) -> None:
        """
        In a wrapped phase array, replaces the two points before
        each wrap with NaN. This is useful to prevent matplotlib
        from plotting vertical lines at the wrap locations.

        Not ideal but works while waiting for a better way of
        disabling the vertical lines
        """

        # Get sign of each point
        # Negative  gives -1
        # Positive  gives 1
        # Zero      gives 0
        signs = np.sign(self.filter['phase_deg'])

        # Split the list in adjacent pairs
        pairs = []
        for i in range(len(signs) - 1):
            pairs.append( (signs[i], signs[i + 1]) )

        # A pair of (-1, 1) indicates a wrap: find out the indexes of such pairs
        pairs_indexes = [index for index, element in enumerate(pairs) if element == (-1, 1) or element == (1, -1)]

        # Replace all points before the wraps with NaN
        self.filter['phase_deg_nan'] = self.filter['phase_deg'].copy()
        self.filter['phase_deg_nan'][pairs_indexes] = np.nan

    def wrap_phase(self) -> None:
        """
        Wraps the phase data to fit in the [-180, 180] range
        """

        self.filter['phase_deg'] = ((self.filter['phase_deg'] + 180) % 360) - 180
        self.filter['phase_rad'] = ((self.filter['phase_rad'] + np.pi) % (2 * np.pi)) - np.pi

    def generate_zpk(self) -> None:
        """
        Generates zero, poles and gain from the transfer function
        """

        self.z, self.p, self.k = sos2zpk(self.sos)

    def compute_group_delay(self) -> None:

        group_delay = (
            -np.diff(np.unwrap(self.get_phase_rad()))
            / np.diff(2 * np.pi * self.get_frequencies())
        )
        group_delay_ms = group_delay * 1000

        self.filter['group_delay_ms'] = group_delay_ms

    def set_flip_phase(self, flip_phase: bool) -> None:

        self.flip_phase = flip_phase

    def get_flip_phase(self) -> None:

        return self.flip_phase