from PyQt6.QtCore import QObject
import numpy as np

class GraphEngine(QObject):
    """
    Base class for computing the data to display in a graph

    Must be inherited by a child class implementing the
    virtual method(s)
    """

    def __init__(self,
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self.filter = {
            "frequencies": [],
            "magnitude": [],
            "phase": []
        }

        self.fs = 48000
        self.frequency_points = 5000

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