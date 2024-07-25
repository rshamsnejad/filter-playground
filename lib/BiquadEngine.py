from lib.GraphEngine import GraphEngine
from scipy.signal import butter, freqz
from numpy import logspace, log10, angle, pi, sin, cos, sqrt

class BiquadEngine(GraphEngine):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def compute(self) -> None:
        self.w0 = 2 * pi * self.get_cutoff() / self.fs
        self.Q = sqrt(2) / 2
        self.alpha = sin(self.w0) / (2 * self.Q)

        if self.get_filtertype().lower() in ["highpass", "lowpass"]:
            b, a = butter(self.order, self.cutoff, self.filtertype, fs=self.fs)

        elif self.get_filtertype().lower() == "allpass":
            b = [1 - self.alpha, -2 * cos(self.w0), 1 + self.alpha]
            a = [1 + self.alpha, -2 * cos(self.w0), 1 - self.alpha]

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
        if self.get_filtertype().lower() in ["highpass", "lowpass"]:
            type_string = (
                f"Butterworth {self.get_filtertype().lower()} filter"
                f", order {self.get_order()}"
            )
        elif self.get_filtertype().lower() == "allpass":
            type_string = f"Biquad allpass filter, order 2, Q = {self.Q:.2f}"

        return type_string + (
            f", $f_0 = {self.get_cutoff()}$ Hz"
        )
