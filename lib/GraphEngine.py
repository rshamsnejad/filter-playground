from PyQt6.QtCore import QObject
import numpy as np

class GraphEngine(QObject):
    def __init__(self,
        filtertype: str = "highpass",
        order:      int = 2,
        frequency:     float = 1000,
        gain:       float = 3,
        Q:          float = 0.71,
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self.set_order(order)
        self.set_frequency(frequency)
        self.set_filtertype(filtertype)
        self.set_gain(gain)
        self.set_Q(Q)

        self.filter = {
            "frequencies": [],
            "magnitude": [],
            "phase": []
        }

        self.fs = 48000
        self.frequency_points = 5000

    def set_filtertype(self, filtertype: str) -> None:
        if filtertype.casefold() not in ["highpass", "lowpass", "allpass"]:
            self.filtertype = "highpass"
            raise ValueError("Incorrect filter type")
        else:
            self.filtertype = filtertype

    def get_filtertype(self) -> str:
        return self.filtertype

    def set_order(self, order: int) -> None:
        if order <= 0:
            self.order = 1
            raise ValueError("Order must be a positive integer")
        else:
            self.order = order

    def get_order(self) -> int:
        return self.order

    def set_frequency(self, frequency: float) -> None:
        if frequency < 1:
            self.frequency = 1000
            raise ValueError("Frequency must be a positive value")
        else:
            self.frequency = frequency

    def get_frequency(self) -> float:
        return self.frequency

    def set_gain(self, gain: float) -> None:
        self.gain = gain

    def get_gain(self) -> float:
        return self.gain

    def set_Q(self, Q: float) -> None:
        if Q <= 0:
            self.Q = 0.71
            raise ValueError("Q must be a positive value")
        else:
            self.Q = Q

    def compute(self) -> None:
        '''
        Must be implemented by child classes
        '''
        raise NotImplementedError

    def generate_title(self) -> str:
        '''
        Must be implemented by child classes
        '''
        raise NotImplementedError

    def get_frequencies(self) -> list[float]:
        return self.filter['frequencies']

    def get_magnitude(self) -> list[float]:
        return self.filter['magnitude']

    def get_phase(self) -> list[float]:
        return self.filter['phase']

    def remove_phase_discontinuities(self) -> None:
        """
        In a wrapped phase array, replaces the two points before
        each wrap with NaN. This is useful to prevent matplotlib
        from plotting vertical lines at the wrap locations
        """

        # Get sign of each point
        # Negative  gives -1
        # Positive  gives 1
        # Zero      gives 0
        signs = np.sign(self.filter['phase'])

        # Split the list in adjacent pairs
        pairs = []
        for i in range(len(signs) - 1):
            pairs.append( (signs[i], signs[i + 1]) )

        # A pair of (-1, 1) indicates a wrap: find out the indexes of such pairs
        pairs_indexes = [index for index, element in enumerate(pairs) if element == (-1, 1) or element == (1, -1)]

        # Replace all points before the wraps with NaN
        self.filter['phase'][pairs_indexes] = np.nan

    def wrap_phase(self) -> None:
        self.filter['phase'] = ((self.filter['phase'] + 180) % 360) - 180