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
        id:         int = 0,
        gain:       float = 0,
        flip_phase: bool = False,
        delay:      int = 0,
        *args, **kwargs
    ) -> None:
        """
        Args:
            gain (float, optional): Overall gain to apply. Defaults to 0.
            flip_phase (bool, optional): Flip phase status. Defaults to False.
        """

        super().__init__(*args, **kwargs)

        self.filter = {
            "frequencies": [],
            "magnitude": [],
            "magnitude_lin": [],
            "magnitude_db": [],
            "phase_rad": [],
            "phase_deg": [],
            "phase_deg_nan": [],
            "phase_delay_ms": [],
            "group_delay_ms": []
        }

        self.set_sample_frequency(48000)
        self.frequency_points = 5000
        self.id = id
        self.set_gain(gain)
        self.set_flip_phase(flip_phase)
        self.set_delay(delay)

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
        self.compute_phase_delay()
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

    def get_phase_delay_ms(self) -> list[float]:
        """
        Returns:
            list[float]: The Y axis phase delay values in ms
        """

        return self.filter['phase_delay_ms']

    def get_group_delay_ms(self) -> list[float]:
        """
        Returns:
            list[float]: The Y axis group delay values in ms
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

    def compute_phase_delay(self) -> None:

        phase_delay = -np.unwrap(self.get_phase_rad()) / (2 * np.pi * self.get_frequencies())
        phase_delay_ms = phase_delay * 1000

        self.filter['phase_delay_ms'] = phase_delay_ms

    def compute_group_delay(self) -> None:

        group_delay = (
            -np.diff(np.unwrap(self.get_phase_rad()))
            / np.diff(2 * np.pi * self.get_frequencies())
        )
        group_delay_ms = group_delay * 1000

        self.filter['group_delay_ms'] = group_delay_ms

    def set_sample_frequency(self, sample_frequency: float) -> None:
        """
        Args:
            sample_frequency (float): The sample frequency in Hertz
        """

        if sample_frequency <= 0:
            self.fs = 48000
            raise ValueError("Sample frequency must be a positive value")
        else:
            self.fs = sample_frequency

    def get_sample_frequency(self) -> float:
        """
        Returns:
            float: The current sample frequency in Hertz
        """

        return self.fs

    def set_flip_phase(self, flip_phase: bool) -> None:
        """
        Args:
            flip_phase (bool): The flip phase status
        """

        self.flip_phase = flip_phase

    def get_flip_phase(self) -> bool:
        """
        Returns:
            bool: The current flip phase status
        """

        return self.flip_phase

    def set_gain(self, gain: float) -> None:
        """
        Args:
            gain (float): The filter gain in dB
        """

        self.gain = gain

    def get_gain(self) -> float:
        """
        Returns:
            float: The current filter gain in dB
        """

        return self.gain

    def set_delay(self, delay: int) -> None:
        """
        Args:
            delay (int): The delay in samples
        """

        self.delay = delay

    def get_delay(self) -> int:
        """
        Returns:
            int: The current delay in samples
        """

        return self.delay

    def process_flip_phase(self) -> None:
        """
        Applies the phase flip to the current transfer function
        """

        if self.get_flip_phase():
            self.sos[0][0] *= -1
            self.sos[0][1] *= -1
            self.sos[0][2] *= -1

    def process_gain(self, gain_offset_db: float) -> None:
        """
        Applies a gain to the current transfer function

        Args:
            gain_offset_db (float): The gain to apply in dB
        """

        gain_offset_lin = 10 ** (gain_offset_db / 20)

        self.sos[0][0] *= gain_offset_lin
        self.sos[0][1] *= gain_offset_lin
        self.sos[0][2] *= gain_offset_lin
    def process_delay(self, delay_samples: int) -> None:
        """
        Applies a delay to the current transfer function

        Args:
            delay_samples (int): The delay to apply in samples
        """

        sos_delay_1sample = [[0, 1, 0, 1, 0, 0]]

        if delay_samples == 0:
            return

        else:
            delay_sos = list(sos_delay_1sample)

            for i in range(delay_samples - 1):
                delay_sos.extend(sos_delay_1sample)

            self.sos = list(self.sos)
            self.sos.extend(delay_sos)
