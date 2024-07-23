from PyQt6.QtCore import QObject
import numpy as np

class GraphEngine(QObject):
    def __init__(self,
        order:      int = 4,
        cutoff:     float = 1000,
        filtertype: str = "highpass",
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self.set_order(order)
        self.set_cutoff(cutoff)
        self.set_filtertype(filtertype)

        self.filter = {
            "frequencies": [],
            "magnitude": [],
            "phase": []
        }

    def set_order(self, order: int) -> None:
        if order <= 0:
            self.order = 1
            raise ValueError("Order must be a positive integer")
        else:
            self.order = order

    def get_order(self) -> int:
        return self.order

    def set_cutoff(self, cutoff: float) -> None:
        if cutoff < 1:
            self.cutoff = 1000
            raise ValueError("Cutoff must be a positive value")
        else:
            self.cutoff = cutoff

    def get_cutoff(self) -> float:
        return self.cutoff

    def set_filtertype(self, filtertype: str) -> None:
        if filtertype.casefold() not in ["highpass", "lowpass", "bandpass", "bandstop"]:
            self.filtertype = "highpass"
            raise ValueError("Incorrect filter type")
        else:
            self.filtertype = filtertype

    def get_filtertype(self) -> str:
        return self.filtertype

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
