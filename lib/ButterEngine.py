from lib.GraphEngine import GraphEngine
from scipy.signal import butter, freqz
from numpy import logspace, log10, angle

class ButterEngine(GraphEngine):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def compute(self) -> None:
        b, a = butter(self.order, self.cutoff, self.filtertype, fs=self.fs)
        frequencies, magnitude = freqz(b, a, worN=logspace(0, 5, 1000), fs=self.fs)

        mag_db = 20 * log10(abs(magnitude))
        phase_deg = angle(magnitude, deg=True)

        self.filter = {
            "frequencies": frequencies,
            "magnitude": mag_db,
            "phase": phase_deg
        }

        self.remove_phase_discontinuities()

    def generate_title(self) -> str:
        return (
            f"Butterworth {self.get_filtertype().lower()} filter, "
            f"order {self.get_order()}, "
            f"$f_0 = {self.get_cutoff()}$ Hz"
        )
