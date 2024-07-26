from PyQt6.QtCore import QObject
import numpy as np

class GraphEngine(QObject):
    """
    Base class for computing the data to display in a graph

    Must be inherited by a child class implementing the
    virtual method(s)
    """

    def __init__(self,
        filtertype: str = "highpass",
        order:      int = 2,
        frequency:     float = 1000,
        gain:       float = 0,
        Q:          float = 0.71,
        *args, **kwargs
    ) -> None:
        """
        Args:
            filtertype (str, optional):
                String representing the filter type. Defaults to "highpass".
            order (int, optional):
                Filter order. Defaults to 2.
            frequency (float, optional):
                Filter's charateristic frequency. Defaults to 1000.
            gain (float, optional):
                Filter's gain. Defaults to 0.
            Q (float, optional):
                Filter's quality factor. Defaults to 0.71.
        """

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
        """
        Args:
            filtertype (str): String representing the filter type

        Raises:
            ValueError: Raised in case of an invalid string
        """

        if filtertype.casefold() not in [
            "highpass",
            "lowpass",
            "allpass",
            "peak",
            "highshelf",
            "lowshelf"
        ]:
            self.filtertype = "highpass"
            raise ValueError("Incorrect filter type")
        else:
            self.filtertype = filtertype

    def get_filtertype(self) -> str:
        """
        Returns:
            str: String representing the current filter type
        """
        return self.filtertype

    def set_order(self, order: int) -> None:
        """
        Args:
            order (int): Filter order

        Raises:
            ValueError: In case of a zero or negative number
        """

        if order <= 0:
            self.order = 1
            raise ValueError("Order must be a positive integer")
        else:
            self.order = order

    def get_order(self) -> int:
        """
        Returns:
            int: The current filter order
        """

        return self.order

    def set_frequency(self, frequency: float) -> None:
        """
        Args:
            frequency (float): The filter frequency

        Raises:
            ValueError: In case of a zero or negative number
        """

        if frequency <= 0:
            self.frequency = 1000
            raise ValueError("Frequency must be a positive value")
        else:
            self.frequency = frequency

    def get_frequency(self) -> float:
        """
        Returns:
            float: The current filter frequency
        """

        return self.frequency

    def set_gain(self, gain: float) -> None:
        """
        Args:
            gain (float): The filter gain
        """

        self.gain = gain

    def get_gain(self) -> float:
        """
        Returns:
            float: The current filter gain
        """

        return self.gain

    def set_Q(self, Q: float) -> None:
        """
        Args:
            Q (float): The filter quality factor

        Raises:
            ValueError: In case of a zero or negative number
        """

        if Q <= 0:
            self.Q = 0.71
            raise ValueError("Q must be a positive value")
        else:
            self.Q = Q

    def compute(self) -> None:
        """
        Compute the filter data based on the parameters.

        Must be implemented by child classes
        """

        raise NotImplementedError

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
            list[float]: The Y axis magnitude values
        """

        return self.filter['magnitude']

    def get_phase(self) -> list[float]:
        """
        Returns:
            list[float]: The Y axis phase values
        """

        return self.filter['phase']

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
        """
        Wraps the phase data to fit in the [-180, 180] range
        """

        self.filter['phase'] = ((self.filter['phase'] + 180) % 360) - 180