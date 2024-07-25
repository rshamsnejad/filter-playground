from lib.GraphEngine import GraphEngine
from scipy.signal import butter, freqz
from numpy import logspace, log10, angle, pi, sin, cos, sqrt, tan, convolve

class BiquadEngine(GraphEngine):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def compute(self) -> None:
        self.w0 = 2 * pi * self.get_cutoff() / self.fs
        self.Q = sqrt(2) / 2
        self.alpha = sin(self.w0) / (2 * self.Q)

        if self.get_filtertype().lower() in ["highpass", "lowpass"]:
            self.b, self.a = butter(self.order, self.cutoff, self.filtertype, fs=self.fs)

        elif self.get_filtertype().lower() == "allpass":
            coeff1 = (tan(pi * self.get_cutoff()/self.fs) - 1) / (tan(pi * self.get_cutoff()/self.fs) + 1)
            b_order1 = [coeff1, 1]
            a_order1 = [1, coeff1]
            b_order2 = [1 - self.alpha, -2 * cos(self.w0), 1 + self.alpha]
            a_order2 = [1 + self.alpha, -2 * cos(self.w0), 1 - self.alpha]

            if self.get_order() == 1:
                self.b = b_order1
                self.a = a_order1
            elif self.get_order() == 2:
                self.b = b_order2
                self.a = a_order2
            else:
                # Odd order of 3 or more
                if self.get_order() % 2 == 1:
                    iterations = (self.get_order() - 1) / 2

                    self.b = b_order1
                    self.a = a_order1
                # Even order of 4 or more
                else:
                    iterations = self.get_order() / 2

                    self.b = b_order2
                    self.a = b_order2

                for i in range(int(iterations)):
                    self.b = convolve(self.b, b_order2)
                    self.a = convolve(self.a, a_order2)

        frequencies, magnitude = freqz(self.b, self.a, worN=logspace(0, 5, 1000), fs=self.fs)

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
            type_string = f"Biquad allpass filter, order {self.get_order()}, Q = {self.Q:.2f}"

        return type_string + (
            f", $f_0 = {self.get_cutoff()}$ Hz"
        )
