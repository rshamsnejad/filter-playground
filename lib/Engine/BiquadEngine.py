from tracemalloc import stop
from lib.Engine.GraphEngine import GraphEngine
from scipy.signal import butter, bessel, cheby1, cheby2, ellip, sosfreqz, tf2sos
from numpy import log10, angle, pi, sin, cos, sqrt, tan

class BiquadEngine(GraphEngine):
    """
    Child class to compute an input cell's biquad filter
    """

    def __init__(self,
        filtertype:             str = "highpass",
        order:                  int = 2,
        frequency:              int = 1000,
        Q:                      float = 0.71,
        passband_ripple:        float = 3,
        stopband_attenuation:   float = 60,
        *args, **kwargs
    ) -> None:
        """
        Args:
            filtertype (str, optional):
                String representing the filter type.
                Defaults to "highpass".
            order (int, optional):
                Filter order.
                Defaults to 2.
            frequency (int, optional):
                Filter's charateristic frequency. Defaults to 1000.
            Q (float, optional):
                Filter's quality factor.
                Defaults to 0.71.
            passband_ripple (float, optional):
                Maximum passband ripple under 0 dB.
                For Chebyshev I and Elliptic filters only.
                Defaults to 3.
            stopband_attenuation (float, optional):
                Minimum stopband attenuation.
                For Chebyshev II and Elliptic filters only.
                Defaults to 60.
        """

        super().__init__(*args, **kwargs)

        self.set_order(order)
        self.set_frequency(frequency)
        self.set_filtertype(filtertype)
        self.set_Q(Q)
        self.set_passband_ripple(passband_ripple)
        self.set_stopband_attenuation(stopband_attenuation)

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
            "lowshelf",
            "highshelf",
            "butterworth highpass",
            "butterworth lowpass",
            "bessel highpass",
            "bessel lowpass",
            "chebyshev i highpass",
            "chebyshev i lowpass",
            "chebyshev ii highpass",
            "chebyshev ii lowpass",
            "elliptic highpass",
            "elliptic lowpass"
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

        if frequency <= 0 or frequency >= self.get_sample_frequency() / 2:
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

    def set_passband_ripple(self, passband_ripple: float) -> None:
        """
        For Chebyshev I and Elliptic filters only

        Args:
            passband_ripple (float): Maximum passband ripple in dB
        """

        if passband_ripple < 0:
            self.passband_ripple = 3
            raise ValueError("Passband ripple must be a positive value")
        else:
            self.passband_ripple = passband_ripple

    def get_passband_ripple(self) -> float:
        """
        Returns:
            float: The current passband ripple
        """

        return self.passband_ripple

    def set_stopband_attenuation(self, stopband_attenuation: float) -> None:
        """
        For Chebyshev II and Elliptic filters only

        Args:
            stopband_attenuation (float): The minimum stopband attenuation in dB
        """

        if stopband_attenuation < 0:
            self.stopband_attenuation = 60
            raise ValueError("Stopband attenuation must be a positive value")
        else:
            self.stopband_attenuation = stopband_attenuation

    def get_stopband_attenuation(self) -> float:
        """
        Returns:
            float: The current stopband attenuation
        """

        return self.stopband_attenuation

    def compute_specific(self) -> None:
        """
        Compute the specific filter data based on the parameters.

        References :
            * https://webaudio.github.io/Audio-EQ-Cookbook/audio-eq-cookbook.html
            * https://thewolfsound.com/allpass-filter/
        """

        self.w0 = 2 * pi * self.get_frequency() / self.get_sample_frequency()
        self.alpha = sin(self.w0) / (2 * self.get_Q())
        self.A = 10**(self.get_gain() / 40)

        gain_offset_db = self.get_gain()

        match self.get_filtertype().lower():
            case "highpass":
                b = [ (1 + cos(self.w0)) / 2, -(1 + cos(self.w0)), (1 + cos(self.w0)) / 2 ]
                a = [ 1 + self.alpha, -2 * cos(self.w0), 1 - self.alpha ]
                self.sos = tf2sos(b, a)

            case "lowpass":
                b = [ (1 - cos(self.w0)) / 2, 1 - cos(self.w0), (1 - cos(self.w0)) / 2 ]
                a = [ 1 + self.alpha, -2 * cos(self.w0), 1 - self.alpha ]
                self.sos = tf2sos(b, a)

            case "allpass":
                coeff1 = (tan(pi * self.get_frequency()/self.get_sample_frequency()) - 1) / (tan(pi * self.get_frequency()/self.get_sample_frequency()) + 1)
                b_order1 = [coeff1, 1, 0]
                a_order1 = [1, coeff1, 0]
                sos_order1 = list(tf2sos(b_order1, a_order1))
                b_order2 = [1 - self.alpha, -2 * cos(self.w0), 1 + self.alpha]
                a_order2 = [1 + self.alpha, -2 * cos(self.w0), 1 - self.alpha]
                sos_order2 = list(tf2sos(b_order2, a_order2))

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
                        self.sos.extend(sos_order2)

                gain_offset_db = 0

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

                gain_offset_db = 0

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

                gain_offset_db = 0

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

                gain_offset_db = 0

            case "butterworth highpass" | "butterworth lowpass":
                self.sos = butter(
                    N=self.get_order(),
                    Wn=self.get_frequency(),
                    btype=self.get_filtertype().lower().replace("butterworth ", ""),
                    analog=False,
                    output='sos',
                    fs=self.get_sample_frequency()
                )

            case "bessel highpass" | "bessel lowpass":
                self.sos = bessel(
                    N=self.get_order(),
                    Wn=self.get_frequency(),
                    btype=self.get_filtertype().lower().replace("bessel ", ""),
                    analog=False,
                    output='sos',
                    norm='mag',
                    fs=self.get_sample_frequency()
                )

            case "chebyshev i highpass" | "chebyshev i lowpass":
                self.sos = cheby1(
                    N=self.get_order(),
                    rp=self.get_passband_ripple(),
                    Wn=self.get_frequency(),
                    btype=self.get_filtertype().lower().replace("chebyshev i ", ""),
                    analog=False,
                    output='sos',
                    fs=self.get_sample_frequency()
                )

            case "chebyshev ii highpass" | "chebyshev ii lowpass":
                self.sos = cheby2(
                    N=self.get_order(),
                    rs=self.get_stopband_attenuation(),
                    Wn=self.get_frequency(),
                    btype=self.get_filtertype().lower().replace("chebyshev ii ", ""),
                    analog=False,
                    output='sos',
                    fs=self.get_sample_frequency()
                )

            case "elliptic highpass" | "elliptic lowpass":
                self.sos = ellip(
                    N=self.get_order(),
                    rp=self.get_passband_ripple(),
                    rs=self.get_stopband_attenuation(),
                    Wn=self.get_frequency(),
                    btype=self.get_filtertype().lower().replace("elliptic ", ""),
                    analog=False,
                    output='sos',
                    fs=self.get_sample_frequency()
                )

            case _:
                raise ValueError("Unknown filter type")

        self.process_gain(gain_offset_db)
        self.process_flip_phase()

        frequencies, magnitude = sosfreqz(self.sos, worN=self.frequency_points, fs=self.get_sample_frequency())

        mag_lin = abs(magnitude)
        mag_db = 20 * log10(abs(magnitude))
        phase_rad = angle(magnitude, deg=False)
        phase_deg = angle(magnitude, deg=True)

        self.filter = {
            "frequencies": frequencies,
            "magnitude": magnitude,
            "magnitude_lin": mag_lin,
            "magnitude_db": mag_db,
            "phase_rad": phase_rad,
            "phase_deg": phase_deg
        }

    def generate_title(self) -> str:
        """
        Create a string to display as graph title.
        """

        match self.get_filtertype().lower():
            case "highpass" | "lowpass":
                type_string = f"Biquad {self.get_filtertype().lower()} filter"

            case "allpass":
                type_string = (
                    f"Biquad allpass filter"
                    # ", order {self.get_order()}, Q = {self.get_Q():.2f}"
                )

            case "peak":
                type_string = "Biquad peaking EQ"

            case "lowshelf":
                type_string = "Biquad low shelf EQ"

            case "highshelf":
                type_string = "Biquad high shelf EQ"

            case "bessel highpass" | "bessel lowpass" \
                | "butterworth highpass" | "butterworth lowpass" \
                | "chebyshev i highpass" | "chebyshev i lowpass" \
                | "chebyshev ii highpass" | "chebyshev ii lowpass" \
                | "elliptic highpass" | "elliptic lowpass":
                type_string = f"{self.get_filtertype()} filter"

            case _:
                raise ValueError("Unknown filter type")

        return type_string # + f", $f_0 = {self.get_frequency()}$ Hz"
