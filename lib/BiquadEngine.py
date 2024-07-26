from lib.GraphEngine import GraphEngine
from scipy.signal import butter, freqz
from numpy import log10, angle, pi, sin, cos, tan, convolve

class BiquadEngine(GraphEngine):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def compute(self) -> None:
        self.w0 = 2 * pi * self.get_frequency() / self.fs
        self.alpha = sin(self.w0) / (2 * self.Q)
        self.A = 10**(self.get_gain() / 40)

        match self.get_filtertype().lower():
            case "highpass" | "lowpass":
                self.b, self.a = butter(self.get_order(), self.get_frequency(), self.get_filtertype(), fs=self.fs)

            case "allpass":
                coeff1 = (tan(pi * self.get_frequency()/self.fs) - 1) / (tan(pi * self.get_frequency()/self.fs) + 1)
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

            case "peak":
                self.b = [
                    1 + self.alpha * self.A,
                    -2 * cos(self.w0),
                    1 - self.alpha * self.A
                ]
                self.a = [
                    1 + self.alpha / self.A,
                    -2 * cos(self.w0),
                    1 - self.alpha / self.A
                ]

            case _:
                raise ValueError("Unknown filter type")

        frequencies, magnitude = freqz(self.b, self.a, worN=self.frequency_points, fs=self.fs)

        mag_db = 20 * log10(abs(magnitude))
        phase_deg = angle(magnitude, deg=True)

        self.filter = {
            "frequencies": frequencies,
            "magnitude": mag_db,
            "phase": phase_deg
        }

        self.remove_phase_discontinuities()

    def generate_title(self) -> str:
        match self.get_filtertype().lower():
            case "highpass" | "lowpass":
                type_string = (
                    f"Butterworth {self.get_filtertype().lower()} filter"
                    # f", order {self.get_order()}"
                )

            case "allpass":
                type_string = (
                    f"Biquad allpass filter"
                    # ", order {self.get_order()}, Q = {self.Q:.2f}"
                )

            case "peak":
                type_string = "Biquad peaking EQ"

            case _:
                raise ValueError("Unknown filter type")

        return type_string # + f", $f_0 = {self.get_frequency()}$ Hz"
