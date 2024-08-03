from lib.Engine.GraphEngine import GraphEngine
from scipy.signal import butter, sosfreqz, tf2sos
from numpy import log10, angle, pi, sin, cos, sqrt, tan

class BiquadEngine(GraphEngine):
    """
    Child class to compute an input cell's biquad filter
    """

    def __init__(self,
        filtertype: str = "highpass",
        order:      int = 2,
        frequency:  int = 1000,
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
            frequency (int, optional):
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

    def set_frequency(self, frequency: int) -> None:
        """
        Args:
            frequency (int): The filter frequency

        Raises:
            ValueError: In case of value out of bounds
        """

        if frequency <= 0 or frequency >= self.fs / 2:
            self.frequency = 1000
            raise ValueError("Frequency must be a positive value under fs/2")
        else:
            self.frequency = frequency

    def get_frequency(self) -> int:
        """
        Returns:
            int: The current filter frequency
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

    def get_Q(self) -> float:
        """
        Returns:
            float: The current filter quality factor
        """

        return self.Q

    def compute(self) -> None:
        """
        Compute the filter data based on the parameters.

        References :
            * https://webaudio.github.io/Audio-EQ-Cookbook/audio-eq-cookbook.html
            * https://thewolfsound.com/allpass-filter/
        """

        self.w0 = 2 * pi * self.get_frequency() / self.fs
        self.alpha = sin(self.w0) / (2 * self.get_Q())
        self.A = 10**(self.get_gain() / 40)

        match self.get_filtertype().lower():
            case "highpass" | "lowpass":
                self.sos = butter(self.get_order(), self.get_frequency(), self.get_filtertype(), fs=self.fs, output='sos')

            case "allpass":
                coeff1 = (tan(pi * self.get_frequency()/self.fs) - 1) / (tan(pi * self.get_frequency()/self.fs) + 1)
                b_order1 = [coeff1, 1, 0]
                a_order1 = [1, coeff1, 0]
                sos_order1 = tf2sos(b_order1, a_order1)
                b_order2 = [1 - self.alpha, -2 * cos(self.w0), 1 + self.alpha]
                a_order2 = [1 + self.alpha, -2 * cos(self.w0), 1 - self.alpha]
                sos_order2 = tf2sos(b_order2, a_order2)

                if self.get_order() == 1:
                    self.sos = sos_order1
                elif self.get_order() == 2:
                    self.sos = sos_order2
                else:
                    # Odd order of 3 or more
                    if self.get_order() % 2 == 1:
                        iterations = (self.get_order() - 1) / 2

                        self.sos = sos_order1
                    # Even order of 4 or more
                    else:
                        iterations = self.get_order() / 2

                        self.sos = sos_order2

                    for i in range(int(iterations)):
                        self.sos.append(sos_order2[0])

            case "peak":
                b = [
                    1 + self.alpha * self.A,
                    -2 * cos(self.w0),
                    1 - self.alpha * self.A
                ]
                a = [
                    1 + self.alpha / self.A,
                    -2 * cos(self.w0),
                    1 - self.alpha / self.A
                ]
                self.sos = tf2sos(b, a)

            case "highshelf":
                b = [
                    self.A * ( self.A + 1 + (self.A - 1) * cos(self.w0) + 2 * sqrt(self.A) * self.alpha ),
                    -2 * self.A * ( self.A - 1 + (self.A + 1) * cos(self.w0) ),
                    self.A * ( self.A + 1 + (self.A - 1) * cos(self.w0) - 2 * sqrt(self.A) * self.alpha )
                ]
                a = [
                    self.A + 1 - (self.A - 1) * cos(self.w0) + 2 * sqrt(self.A) * self.alpha,
                    2 * ( self.A - 1 - (self.A + 1) * cos(self.w0) ),
                    self.A + 1 - (self.A - 1) * cos(self.w0) - 2 * sqrt(self.A) * self.alpha
                ]
                self.sos = tf2sos(b, a)

            case "lowshelf":
                b = [
                    self.A * ( self.A + 1 - (self.A - 1) * cos(self.w0) + 2 * sqrt(self.A) * self.alpha ),
                    2 * self.A * ( self.A - 1 - (self.A + 1) * cos(self.w0) ),
                    self.A * ( self.A + 1 - (self.A - 1) * cos(self.w0) - 2 * sqrt(self.A) * self.alpha )
                ]
                a = [
                    self.A + 1 + (self.A - 1) * cos(self.w0) + 2 * sqrt(self.A) * self.alpha,
                    -2 * ( self.A - 1 + (self.A + 1) * cos(self.w0) ),
                    self.A + 1 + (self.A - 1) * cos(self.w0) - 2 * sqrt(self.A) * self.alpha
                ]
                self.sos = tf2sos(b, a)

            case _:
                raise ValueError("Unknown filter type")

        frequencies, magnitude = sosfreqz(self.sos, worN=self.frequency_points, fs=self.fs)

        mag_db = 20 * log10(abs(magnitude))
        phase_deg = angle(magnitude, deg=True)

        self.filter = {
            "frequencies": frequencies,
            "magnitude": mag_db,
            "phase": phase_deg
        }

        self.remove_phase_discontinuities()

        self.generate_zpk()

    def generate_title(self) -> str:
        """
        Create a string to display as graph title.
        """

        match self.get_filtertype().lower():
            case "highpass" | "lowpass":
                type_string = (
                    f"Butterworth {self.get_filtertype().lower()} filter"
                    # f", order {self.get_order()}"
                )

            case "allpass":
                type_string = (
                    f"Biquad allpass filter"
                    # ", order {self.get_order()}, Q = {self.get_Q():.2f}"
                )

            case "peak":
                type_string = "Biquad peaking EQ"

            case "highshelf":
                type_string = "Biquad high shelf"

            case "lowshelf":
                type_string = "Biquad low shelf"

            case _:
                raise ValueError("Unknown filter type")

        return type_string # + f", $f_0 = {self.get_frequency()}$ Hz"
