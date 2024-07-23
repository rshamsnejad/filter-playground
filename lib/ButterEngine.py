from lib.GraphEngine import GraphEngine
from scipy.signal import butter, freqs
from numpy import logspace, log10, angle

class ButterEngine(GraphEngine):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def compute(self) -> None:
        b, a = butter(self.order, self.cutoff, self.filtertype, True)
        frequencies, magnitude = freqs(b, a, worN=logspace(0, 5, 1000))

        mag_db = 20 * log10(abs(magnitude))
        phase_deg = angle(magnitude, deg=True)
        phase_deg_nan = self.remove_phase_discontinuities(phase_deg)

        self.filter = {
            "frequencies": frequencies,
            "magnitude": mag_db,
            "phase": phase_deg_nan
        }

    def generate_title(self) -> str:
        return (
            f"Butterworth {self.get_filtertype().lower()} filter, "
            f"order {self.get_order()}, "
            f"$f_0 = {self.get_cutoff()}$ Hz"
        )
